# -*- coding: utf-8 -*-

import six

# standard libs
import os
import ssl
# import hashlib
# import hmac
from binascii import unhexlify
from base64 import b32encode
from base64 import b64decode
# import uuid
import datetime
import time
import json
import re
import threading
import logging
import logging.handlers
import smtplib
# import shelve

# require Pillow
from PIL import Image

# import ImageEnhance
# import ImageOps

# require xlwt
import xlwt

# require mathplotlib + numpy
# todo

# pip install digimat.gapi
# from digimat.gapi import GWSheet

# pip install requests
import requests


# pip install pyotp
import pyotp

# General Structure
# RWSClient(->RWSNet)->RWSNode->RWSItem

API_WRAPPER_VENDOR='Digimat'
API_WRAPPER_NAME='RWS-API Python-Wrapper'
API_WRAPPER_VERSION='1.0.2'

UNIT_STR = ["V", "C", "Pa", "kPa", "%", "l/h", "bar", "Hz",
    "s", "ms", "min", "kW", "kWh", "J", "kJ", "",
    "m/s", "'", "h", "MWh", "MJ", "GJ", "W", "MW",
    "kJ/h", "MJ/h", "GJ/h", "ml", "l", "m3", "ml/h", "m3/h",
    "Wh", "?", "K", "", "lx", "t/min", "kvar", "kvarh",
    "mbar", "msg/m", "m", "kJ/kg", "g/kg", "ppm", "A", "kVA",
    "kVAh", "ohm"]


class Event(object):
    def __init__(self):
        self.handlers = []

    def add(self, handler):
        self.handlers.append(handler)
        return self

    def remove(self, handler):
        self.handlers.remove(handler)
        return self

    def fire(self, sender, earg=None):
        for handler in self.handlers:
            handler(sender, earg)

    __iadd__ = add
    __isub__ = remove
    __call__ = fire


class RWSResponse:
    def __init__(self, rws):
        self._rws=rws
        self._type=None
        self._error=9999
        self._data=None

    @property
    def logger(self):
        return self._rws.logger

    def decodeRequest(self, r):
        try:
            # print(r)
            try:
                self._type=r.headers['Content-Type']
            except:
                self._type='application/json'

            if self._type.find('application/json')>=0:
                self._type='json'
                self._error=0
                jdata=r.text
                if jdata and jdata != 'null':
                    self._data=json.loads(jdata)
                    self.logger.debug("RX-JSON:\n{0}".format(
                      json.dumps(self._data, sort_keys=True, indent=2, separators=(',', ': '))
                      )
                    )
                    try:
                        self._error=self._data['error']
                    except:
                        pass
            elif self._type.find('image/')>=0:
                self._type='image'
                image=Image.open(six.BytesIO(r.content))
                if image:
                    self._error=0
                    self._data=image
            elif self._type.find('text;')>=0 or self._type.find('text/plain')>=0:
                self._error=0
                self._type='text'
                self._data=r.text
                # self.logger.debug("RX-TEXT:{0}".format(self._data))
            else:
                # print "RX-Unknown type"
                # print self._type
                pass
        except:
            self.logger.exception('decodeRequest()')
            self.logger.debug(self._data)
            # print self._data

        if not self.success():
            self.logger.error('unable to decode request!')

        return self._data

    def type(self):
        return self._type

    def typeImage(self):
        return self._type=='image'

    def json(self):
        if self._type=='json':
            return self._data
        return None

    def text(self):
        if self._type=='text':
            return self._data
        return None

    def attr(self, name, default=None):
        try:
            return self.json()[name]
        except:
            pass
        return default

    def error(self):
        return self._error

    def success(self):
        return self.error()==0

    def authFailed(self):
        return self._error==1 or self._error==3


class RWSContext:
    def __init__(self, user, password):
        self._user=user
        self._password=password

    def user(self):
        return self._user

    def password(self):
        return self._password


class RWSClient:
    def __init__(self, serverURL, username=None, password=None, otpSeed=None, logServer='localhost', logLevel=logging.DEBUG):
        self._serverURL=serverURL
        self._username=username
        self._password=password
        self._context=None
        self._otpSeed=b32encode(unhexlify(otpSeed))
        self._networks={}
        self._nodes={}
        self._token=0
        self._jsonEncoder=json.JSONEncoder()

        logger=logging.getLogger("RWSClient(%s)" % username)
        logger.setLevel(logLevel)
        socketHandler = logging.handlers.SocketHandler(logServer, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(socketHandler)
        self._logger=logger
        logging.captureWarnings(True)

        # todo: maybe not a good idea : avoid certificate warning
        ssl._create_default_https_context = ssl._create_unverified_context

    def __del__(self):
        self.dispose()

    def dispose(self):
        # self.disconnect()
        pass

    def info(self):
        return '{0} {1} v{2}'.format(API_WRAPPER_VENDOR, API_WRAPPER_NAME, API_WRAPPER_VERSION)

    @property
    def logger(self):
        return self._logger

    def imageAsPNGBuffer(self, image):
        try:
            buf=six.BytesIO()
            image.save(buf, format='PNG')
            return buf.getvalue()
        except:
            return None

    def jsonEncode(self, obj):
        return self._jsonEncoder.encode(obj)

    def getHotpToken(self):
        index=self.getUserHotpIndex()
        if index:
            otp = pyotp.HOTP(self._otpSeed)
            n=otp.at(index)
            return str(n).zfill(6)
        return 0

    def getRequestURL(self, request):
        return '{0}[{1}]'.format(request.get_full_url(), request.get_data())

    def buildRequestParams(self, params, context=None):
        if not params:
            params={}

        if isinstance(params, dict):
            if self._token:
                params['tk']=self._token
            if context:
                params['user']=self._context.user()
                params['password']=self._context.password()

        return params

    def processRequest(self, action, params=None, data=None, context=None):
        response=RWSResponse(self)
        url='{0}/api/{1}'.format(self._serverURL, action)
        self.logger.debug(url)

        try:
            params=self.buildRequestParams(params, context)
            r=requests.get(url, params=params, data=data, timeout=5)
            if r and r.status_code == requests.codes.ok:
                response.decodeRequest(r)
                if response.authFailed():
                    self.logger.warning('processRequest() auth failed!')
                    self._token=0
            else:
                print("REQUEST BAD RESPONSE", r, r.status_code)
                self.logger.error('processRequest() bad response')
                self._token=0
        except:
            self.logger.exception('processRequest()')
            self._token=0

        return response

    def processRequestWithContext(self, action, params=None, data=None, context=None, retry=3):
        if retry<=0:
            retry=1

        while retry>0:
            retry-=1
            if not self._token:
                self.logger.warning('processRequestWithContext(): auto connect before request.')
                self.connect()

            if self._token:
                if not context:
                    context=self._context
                response=self.processRequest(action, params, data, context)
                if response.success():
                    return response

                self.logger.error('processRequestWithContext(): retry.')

        return RWSResponse(self)

    def processRequestWithoutContext(self, action, params=None, data=None):
        return self.processRequest(action, params, data)

    def token(self):
        return self._token

    def getUserHotpIndex(self):
        self._token=0
        params={'username': self._username, 'password': self._password}
        return int(self.processRequestWithoutContext('gethotp', params).attr('counter', 0))

    def validateToken(self):
        if not self._token:
            return False

        try:
            if len(self._token)==36:
                return True
        except:
            pass

        return False

    def ping(self, timeout=3):
        try:
            url='%s/api/' % self._serverURL
            r=requests.get(url, timeout=3)
            if r and r.status_code == requests.codes.ok:
                return True
        except:
            self.logger.exception('ping()')
            self.logger.error('rws server ping failed (%s)!' % url)

    def connect(self):
        self._token=0
        if self.ping():
            retry=5
            while retry>0 and self._token==0:
                retry=retry-1
                params={'username': self._username, 'password': self._password, 'otp': self.getHotpToken()}
                self._token=self.processRequestWithoutContext('open', params).attr('tk', 0)
                if self._token==0:
                    time.sleep(2)
            return self.validateToken()

    def disconnect(self):
        self.processRequestWithContext('close')
        self._token=0

    def bindWithContext(self, context):
        oldContext=self._context
        self._context=context
        return oldContext

    def browse(self, keyFilter=None):
        params={'dest': 'DMZDCF', 'query': 'list/network'}
        networks=self.processRequestWithContext('dcf', params).json()
        try:
            if keyFilter:
                regex=re.compile(keyFilter)

                def myfilter(key):
                    if regex.match(key):
                        return True
                networks=list(filter(myfilter, networks))
        except:
            pass
        return networks

    def __getitem__(self, key):
        if key:
            return self.network(key)
        return KeyError()

    def __getattr__(self, name):
        item=self.item(name)
        if item:
            return item

        self.logger.error('RWS.%s attribute error' % name)
        raise AttributeError

    def discover(self):
        items=self.browse()
        for item in items:
            try:
                setattr(self, item, self[item])
            except:
                pass

    def network(self, dest):
        if dest in self._networks:
            return self._networks[dest]
        network=RWSNetwork(self, dest)
        self._networks[dest]=network
        return network

    def node(self, dest):
        if dest in self._nodes:
            return self._nodes[dest]
        node=RWSNode(self, dest)
        self._nodes[dest]=node
        return node

    def nodes(self):
        return self._nodes

    def addNode(self, dest):
        return self.node(dest)

    def createItemCollection(self):
        return RWSItemCollection(self)

    def snapshooter(self, fname=None):
        return RWSSnapshoter(self, fname)

    def browser(self, topic=None):
        return RWSBrowser(self, topic)

    def mailer(self):
        return RWSMailer(self)

    def workbook(self):
        return RWSWorkbook(self)

    def contactsheet(self, margin=8, bgColor='lightgray'):
        return RWSContactSheet(self, margin, bgColor)

    def splitItemKey(self, key):
        if key:
            m=re.match('^r_([a-z-A-Z0-9]+)_([a-z-A-Z0-9]+)_([a-zA-Z0-9]+_[@a-zA-Z0-9]+_[a-zA-Z0-9]+)$', key)
            if m:
                kparts={}
                kparts['network']=m.group(1)
                kparts['node']=m.group(2)
                kparts['item']=m.group(3)
                return kparts

    def validateKey(self, key):
        return self.splitItemKey(key)

    def keyPart(self, key, part):
        try:
            kparts=self.splitItemKey(key)
            return kparts[part]
        except:
            pass

    def item(self, key):
        kparts=self.splitItemKey(key)
        if kparts:
            network=self.network(kparts['network'])
            if network:
                node=network.node(kparts['node'])
                if node:
                    item=node.item(kparts['item'])
                    if item:
                        return item

    def value(self, key, default=None):
        try:
            return self.item(key).value
        except:
            return default

    def searchSynopticFromKey(self, key, sfilter=None):
        if self.validateKey(key):
            b=self.browser()
            items=b.searchSynopticFromKey(key, sfilter)
            return items
        else:
            # will accept synoptic path as key (/render synoptic)
            return [key]

    def searchSynopticsFromKeys(self, keys, sfilter=None):
        synoptics=[]
        for key in keys:
            items=self.searchSynopticFromKey(key, sfilter)
            if items:
                for item in items:
                    if item not in synoptics:
                        synoptics.append(item)
        return synoptics

    def renderSynoptic(self, fpath):
        snap=self.snapshooter()
        image=snap.shoot(fpath)
        return image

    def getSynopticImagesFromKey(self, key, maxcount=3):
        try:
            items=self.searchSynopticFromKey(key)
            if items:
                images=[]
                for spath in items[0:maxcount]:
                    images.append(self.renderSynoptic(spath))
                return images
        except:
            pass

    def searchAlarmsFromKey(self, key):
        b=self.browser()
        return b.searchAlarmsFromKey(key)


class RWSWorkbook:
    def __init__(self, rws):
        self._rws=rws
        self._wb=xlwt.Workbook()
        self.initStyles()

    def initStyles(self):
        self._styleDate = xlwt.XFStyle()
        self._styleDate.num_format_str='YYYY-MM-DD HH:MM:SS'

    def addSheetRecord(self, records, name=None):
        if not name:
            name=records.key
        sheet=self._wb.add_sheet(name)
        row=0

        label=records.label
        try:
            unit=UNIT_STR[records.unit]
        except:
            unit=''

        for r in records:
            sheet.row(row).write(0, records.key)
            sheet.row(row).write(1, label)
            sheet.row(row).set_cell_date(2, r['x'], self._styleDate)
            sheet.row(row).write(3, r['y'])
            sheet.row(row).write(4, unit)
            row+=1

        sheet.col(0).width=256*20
        return sheet

    def save(self, fpath):
        ext=os.path.splitext(fpath)[1]
        if not ext:
            fpath += '.xls'
        return self._wb.save(fpath)


class RWSBrowser:
    def __init__(self, rws, topic=None):
        self._rws=rws
        self._installation=0
        self._filter=None
        self._flags=None
        self._topic=topic
        self._results=None
        self.reset()

    @property
    def logger(self):
        return self._rws.logger

    def normalizePath(self, path):
        path=os.path.normpath(path.lower())
        return path

    def topic(self, topic=None):
        if topic is not None and topic!=self._topic:
            self._topic=topic
            self.reset()
        return self._topic

    def variable(self):
        self.topic('variable')

    def synoptic(self):
        self.topic('synoptic')

    def specials(self):
        self.topic('specialstate')

    def reset(self):
        self._index=0
        self._results=[]

    def setFilter(self, filter):
        if filter and filter!=self._filter:
            self._filter=filter
            self.reset()

    def setFlags(self, flags):
        if flags and flags!=self._flags:
            self._flags=flags
            self.reset()

    def setInstallation(self, installation):
        if installation!=self._installation:
            self._installation=installation
            self.reset()

    def storeResults(self, items, pageMaxSize):
        try:
            if not items:
                return 0

            count=items['displayCount']
            # print items

            self._index+=count
            for r in items['r']:
                rtype=r['__type']

                ritem={}
                if rtype=='synoptic':
                    ritem['id']=r['identifier']
                elif rtype=='variable':
                    ritem['key']=r['key']
                    ritem['label']=r['label']
                    ritem['name']=r['name']

                if ritem:
                    self._results.append(ritem)

            if count>=pageMaxSize:
                return True
        except:
            self.logger.exception('storeResults()')
            pass

        return False

    def searchNextPage(self):
        pageMaxSize=512
        params={'topic': self._topic, 'count': pageMaxSize, 'index': self._index}
        if self._filter:
            params['filter']=self._filter
        if self._flags:
            params['flags']=self._flags
        if self._installation:
            params['installation']=self._installation

        items=self._rws.processRequestWithContext('search', params).json()
        return self.storeResults(items, pageMaxSize)

    def search(self, filter, maxCount=0):
        self.setFilter(filter)
        self.reset()
        while self.searchNextPage():
            if maxCount>0 and len(self._results)>=maxCount:
                break
        return self._results

    def searchKey(self, filter, maxCount=0):
        if self._topic=='variable':
            res=self.search(filter, maxCount)
            return [item['key'] for item in res]
        return None

    def searchLabelsFromKey(self, key):
        self.variable()
        r=self.search(key, 1)
        if r and len(r)==1:
            return r[0]

    def searchAlarms(self, maxCount=0):
        self.specials()
        self.setFlags('a')
        return self.search(None, maxCount)

    def searchAlarmsFromKey(self, key, maxCount=0):
        kparts=self._rws.splitItemKey(key)
        if kparts:
            installation=kparts['network']
            self.setInstallation(installation)
            return self.searchAlarms(maxCount)
        else:
            try:
                installation=int(key)
                if installation>0:
                    self.setInstallation(installation)
                    return self.searchAlarms(maxCount)
            except:
                pass

    def searchSynopticFromKey(self, key, sfilter=None):
        synoptics=[]
        try:
            kparts=self._rws.splitItemKey(key)
            if kparts:
                installation=kparts['network']
                self.setInstallation(installation)
                self.synoptic()
                items=self.search(key)
                if items:
                    for i in items:
                        # print i
                        if not sfilter or sfilter in i['id']:
                            synoptics.append(i['id'])
        except:
            pass

        return synoptics


# unicode warning : http://pythonfacile.free.fr/python/unicode.html
class RWSSnapshoter:
    def __init__(self, rws, fpath=None):
        self._rws=rws
        self._fpath=fpath
        self._image=None
        self._autoCrop=True
        self._image=None
        self.reset()

    def reset(self):
        self._image=None

    def setPath(self, fpath):
        if fpath and fpath!=self._fpath:
            self._fpath=fpath
            self.reset()

    def autoCrop(self, state=True):
        self._autoCrop=state

    def crop(self):
        wx, wy = self._image.size
        wx -= 3+2
        wy -= 3+2
        self._image=self._image.crop((3, 3, wx, wy))

    def path(self):
        return self._fpath

    def shoot(self, fpath=None, width=0):
        self.setPath(fpath)
        if self._fpath:
            params={'path': self._fpath}
            if width>0:
                params['width']=width
            response=self._rws.processRequestWithContext('snapshot', params)
            if response and response.typeImage():
                self._image=response._data
                if self._image:
                    if self._autoCrop:
                        self.crop()
        return self._image

    def computeSaveName(self):
        if self._fpath:
            return 'snapshot-' + self._fpath.replace('/', '.') + '.png'
        return None

    def save(self, fpathSave=None):
        if fpathSave:
            self._fpathSave=fpathSave
        if self._fpathSave and self._image:
            # print os.path.expanduser(self._fpathSave)
            return self._image.save(os.path.expanduser(self._fpathSave))
        return False

    def search(self, filter, maxCount=0):
        results=[]

        browser=self._rws.browser('synoptic')
        try:
            items=browser.search(filter)

            for r in items:
                name=r['id']
                if not re.match('[0-9]*/panel.*', name):
                    results.append(name)

                if maxCount>0 and len(self._results)>=maxCount:
                    break
        except:
            pass

        return results


class RWSContactSheetImage:
    def __init__(self):
        self._image=None
        self._rws=None
        self._board=None
        self._parent=None
        self._children=[]
        self._placement='r'
        self._x=0
        self._y=0
        self._margin=5

    @property
    def logger(self):
        return self._rws.logger

    def bbox(self):
        return (self._x, self._y, self._x+self.width()+2*self._margin, self._y+self.height()+2*self._margin)

    def bboxMerge(self, bbox1, bbox2):
        (x00, y00, x01, y01)=bbox1
        (x10, y10, x11, y11)=bbox2
        x0=min(x00, x10)
        x1=max(x01, x11)
        y0=min(y00, y10)
        y1=max(y01, y11)
        return (x0, y0, x1, y1)

    def subbbox(self):
        bbox=self.bbox()
        if self._children:
            for child in self._children:
                bbox=self.bboxMerge(bbox, child.subbbox())
        return bbox

    def margin(self, size=None):
        if size:
            self._margin=size
        return self._margin

    def pos(self):
        return (self._x, self._y)

    def move(self, dx, dy):
        if dx or dy:
            self._x+=dx
            self._y+=dy
            for child in self._children:
                child.move(dx, dy)

    def link(self, child, _placement=None):
        child._rws=self._rws
        child._board=self._board
        child._parent=self
        child._margin=self._margin
        child._placement=_placement
        self._children.append(child)
        return child

    def stickLeft(self, child):
        return self.link(child, 'l')

    def stickRight(self, child):
        return self.link(child, 'r')

    def stickTop(self, child):
        return self.link(child, 't')

    def stickBottom(self, child):
        return self.link(child, 'b')

    def width(self):
        try:
            (wx, wy)=self._image.size
            return wx
        except:
            return 0

    def height(self):
        try:
            (wx, wy)=self._image.size
            return wy
        except:
            return 0

    def rebuildLayout(self):
        for child in self._children:
            if child._placement=='r':
                child._x=self._x+self.width()+self._margin
                child._y=self._y
            elif child._placement=='l':
                child._x=self._x-child.width()-self._margin
                child._y=self._y
            elif child._placement=='t':
                child._x=self._x
                child._y=self._y-child.height()-self._margin
            elif child._placement=='b':
                child._x=self._x
                child._y=self._y+self.height()+self._margin
            child.rebuildLayout()

    def onDraw(self):
        self._image=Image.new("RGB", self.board().cellSize(), 'blue')

    def draw(self):
        try:
            self.onDraw()
        except:
            self.logger.error("RWSBoardImage::onDraw() failure")
        for child in self._children:
            child.draw()
        return self._image

    def image(self):
        return self._image

    def children(self):
        return self._children

    def parent(self):
        return self._parent

    def board(self):
        return self._board

    def compose(self, imageBoard):
        imageBoard.paste(self._image, (self._x+self._margin, self._y+self._margin))
        for child in self._children:
            child.compose(imageBoard)


class RWSContactSheetSynoptic(RWSContactSheetImage):
    def __init__(self, fpath):
        RWSContactSheetImage.__init__(self)
        self._fpath=fpath

    def onDraw(self):
        s=RWSSnapshoter(self._rws)
        self._image=s.shoot(self._fpath, self.board().cellWidth())
        if  not self._image:
            self.logger.error('RWSBoardSynoptic.onDraw({0}):unable to process image'.format(self._path))
        return self._image


class RWSContactSheetSpacer(RWSContactSheetImage):
    def __init__(self, width=0, height=0, bgcolor=None):
        RWSContactSheetImage.__init__(self)
        self._bgcolor=bgcolor
        self._width=width
        self._height=height

    def bgcolor(self, color):
        self._bgcolor=color
        return self._bgcolor

    def onDraw(self):
        wx=self._width
        wy=self._height
        if wx<=0:
            wx=self._parent.width()
        wy=self._height
        if wy<=0:
            wy=self._parent.height()
        bgcolor=self._bgcolor
        if not bgcolor:
            bgcolor=self.board().bgcolor()
        # print('{0},{1}'.format(wx, wy))
        self._image=Image.new("RGB", (wx, wy), bgcolor)


class RWSContactSheet:
    def __init__(self, rws, margin=8, bgColor='lightgray'):
        self._child=None
        self._rws=rws
        self._margin=margin
        self._bgcolor=bgColor
        self._cellSize=(800, 600)
        self._image=None

    def bgcolor(self):
        return self._bgcolor

    def cellSize(self, size=None):
        if size:
            self._cellSize=size
        return self._cellSize

    def cellWidth(self):
        return self.cellSize()[0]

    def cellHeight(self):
        return self.cellSize()[1]

    def stick(self, child):
        child.margin(self._margin)
        child._rws=self._rws
        child._board=self
        self._child=child
        return self._child

    def draw(self):
        self._child.draw()
        self._child.rebuildLayout()

        bbox=self._child.subbbox()
        wx=bbox[2]-bbox[0]
        wy=bbox[3]-bbox[1]

        # normalize bbox
        dx=0
        if bbox[0]<0:
            dx=-bbox[0]
        dy=0
        if bbox[1]<0:
            dy=-bbox[1]
        self._child.move(dx, dy)

        # print("({0},{1},{2},{3})".format(bbox[0], bbox[1], bbox[2], bbox[3]))
        # print("Size {0},{1}".format(wx, wy))

        image=Image.new("RGB", (wx, wy), self._bgcolor)
        self._child.compose(image)
        self._image=image
        return self._image

    def save(self, fpath, redraw=False):
        if redraw or not self._image:
            self.draw()
        try:
            return self._image.save(os.path.expanduser(fpath))
        except:
            return False

    def synoptic(self, fpath):
        return RWSContactSheetSynoptic(fpath)

    def spacer(self, width=0, height=0, bgcolor=None):
        return RWSContactSheetSpacer(width, height, bgcolor)


class RWSMailer:
    def __init__(self, rws):
        self._rws=rws
        self._server=None
        self.reset()

    def setSmtpServer(self, host, user=None, password=None, tls=False):
        self._server={'type': 'smtp', 'host': host, 'user': user, 'password': password, 'tls': tls}

    def setGmailSmtpServer(self, user, password):
        return self.setSmtpServer('smtp.gmail.com:587', user, password, True)

    def connect(self):
        try:
            server=smtplib.SMTP(self._server['host'])
            # server.set_debuglevel(1)

            if self._server['tls']:
                server.starttls()
            if self._server['user']:
                server.login(self._server['user'], self._server['password'])
            else:
                server.connect()
            self._server['instance']=server
            return True
        except:
            return False

    def disconnect(self):
        try:
            self._server['instance'].quit()
            self._server['instance']=None
        except:
            pass

    def getCID(self):
        self._cid+=1
        return 'cdi-{0}'.format(self._cid)

    def attach(self, obj):
        self._attach.append(obj)

    def createMessage(self, subject=None):
        self._message=six.moves.email_mime_multipart.MIMEMultipart(_subtype='related')
        if subject:
            self.setSubject(subject)

    def reset(self):
        self._recipients=[]
        self._attach=[]
        self._cid=0
        self._html=''
        self._style=''
        self.createMessage()

    def setSubject(self, subject):
        self._message['Subject']=subject

    def writeStyle(self, style):
        self._style = self._style + style

    def writeHtml(self, html):
        self._html = self._html + html

    def imageToHtmlSnipet(self, image, format='PNG'):
        if image:
            buf=six.BytesIO()
            image.save(buf, format)
            obj=six.moves.email_mime_image.MIMEImage(buf.getvalue(), image.format)
            buf.close()

            cid=self.getCID()
            obj.add_header('Content-Id', '<{0}>'.format(cid))
            self.attach(obj)
            return "<img src='cid:{0}'/>".format(cid)
        return ''

    def snapshotToHtmlSnipet(self, fpath, width=0):
        snap=self._rws.snapshooter()
        image=snap.shoot(fpath, width)
        return self.imageToHtmlSnipet(image)

    def addRecipient(self, address):
        if address:
            if isinstance(address, str):
                address=address.split(',')
            for a in address:
                if a not in self._recipients:
                    self._recipients.append(a)

    def getHtml(self):
        html="<head>"
        if self._style:
            html += "<style type='text/css'>" + self._style + "</style>"
        html += "</head>"
        html += "<body>" + self._html + "</body>"
        return html

    def send(self, recipients=None):
        result=False
        self.addRecipient(recipients)
        if self._recipients:
            if self.connect():
                originator='Digimat'
                self._message['From']=originator
                self._message['To']=', '.join(self._recipients)

                self._message.attach(six.moves.email_mime_text.MIMEText(self.getHtml(), _subtype='html'))

                if self._attach:
                    for obj in self._attach:
                        self._message.attach(obj)

                try:
                    self._server['instance'].sendmail(originator, self._recipients, self._message.as_string())
                    result=True
                except:
                    pass

                self.disconnect()

        return result


class RWSTask:
    def __init__(self, rws, name, code=None):
        self._name=name
        self._nameTask=self.normalizedName(name)
        self._nameListener='listener.'+self._nameTask
        self._rws=rws
        self._compileResult=None
        self._code=code
        self.debug('Task object created')

    @property
    def logger(self):
        return self._rws.logger

    def __del__(self):
        self.dispose()

    def dispose(self):
        pass

    def normalizedName(self, name):
        name=name.replace(' ', '-')
        name=name.strip()
        name+='.python.wrapper.api.digimat.ch'
        name=os.path.normpath(name)
        return name

    def call(method):
        def rpc(self, *args):
            return self.invokeCall(method.__name__, *args)
        rpc._iscall=True
        return rpc

    def callback(method):
        method._iscallback=True
        return method

    def invokeCallback(self, name, *args):
        try:
            f=getattr(self, name)
            if callable(f) and hasattr(f, '_iscallback'):
                try:
                    f(*args)
                except:
                    self.error('exception occured while invoking callback {0}()'.format(name))

        except:
            self.error('unable to invoke callback {0}()'.format(name))

    def invokeCall(self, name, *args):
        params={'task': self._nameTask}
        fparams=[]
        fparams.append(*args)
        data={'function': name, 'parameters': fparams}
        self._rws.processRequestWithContext('callTask', params, data)

    def read(self):
        params={'task': self._nameTask}
        return self._rws.procesRequest('readTask', params).text()

    def retrieve(self):
        return self.setCode(self.read())

    def compileResult(self):
        return self._compileResult

    def parseCode(self, location):
        try:
            m=re.match('L([0-9]+)C([0-9]+)', location)
            if m:
                line=int(m.group(1))-1
                # col=int(m.group(2))
                return self._code.splitlines()[line]
        except:
            pass
        return None

    def parseCompileResult(self, result):
        try:
            self._compileResult=result
            if not self._compileResult['errors']:
                return True
            for e in self._compileResult['errors']:
                code=self.parseCode(e['location']).strip()
                self.error('{0}:{1}>{2}'.format(e['location'], e['message'], code))
        except:
            pass
        return False

    def setCode(self, code):
        if code is not None:
            self._code=code
        return self._code

    def delete(self):
        self._rws.processRequestWithContext('deleteTask')

    def update(self, code=None):
        self.setCode(code)
        response=self.processRequestWithContext('updateTask', None, self._code)
        if response:
            return self.parseCompileResult(response.json())
        return False

    def create(self, code=None):
        self.setCode(code)
        params={'task': self._nameTask, 'overwrite': 'true'}
        response=self._rws.processRequestWithContext('createTask', params, self._code)
        if response:
            return self.parseCompileResult(response.json())
        return False

    def createFromFile(self, fpath=None):
        result=False
        try:
            if fpath is None:
                fpath='{0}.cs'.format(self._name)
            f=open(fpath)
            try:
                code=f.read()
                result=self.create(code)
            finally:
                f.close()
        except:
            pass

        return result

    def listen(self, timeout=60):
        params={'task': self._nameTask, 'listener': self._nameListener, 'timeout': timeout}
        self.debug('entering listen')
        response=self._rws.processRequestWithContext('listenTask', params).json()
        if response:
            for cb in response:
                try:
                    if cb['__type']=='writeline':
                        self.writeline(cb['message'])
                    elif cb['__type']=='call':
                        p=None
                        try:
                            f=cb['name']
                            p=cb['parameters']
                        except:
                            pass
                        self.debug('Callback {0}()'.format(f))
                        if p:
                            self.invokeCallback(f, *p)
                        else:
                            self.invokeCallback(f)
                except:
                    pass
        self.debug('leaving listen')

    def writeline(self, msg):
        print(msg)
        self.info(msg)

    def log(self):
        params={'task': self._nameTask}
        response=self._rws.processRequestWithContext('taskLog', params)
        return response._data

    def dumpLog(self):
        for l in self.log():
            print(l)

    def dump(self):
        params={'task': self._nameTask}
        response=self._rws.processRequestWithContext('dumpTask', params)
        print((response._data))

    def list(self):
        response=self._rws.processRequestWithContext('listTask')
        print((response._data))

    def logstr(self, msg):
        return '{0}({1}):{2}'.format(self.__class__.__name__, self._nameTask, msg)

    def info(self, msg):
        self.logger.info(self.logstr(msg))

    def debug(self, msg):
        self.logger.debug(self.logstr(msg))

    def warning(self, msg):
        self.logger.warning(self.logstr(msg))

    def error(self, msg):
        self.logger.error(self.logstr(msg))

    @call
    def simpleEcho(self, msg):
        pass

    @callback
    def simpleEchoResponse(self, msg):
        print(msg)

    @callback
    def event(self):
        print("Event Fired!")


class RWSNetwork:
    def __init__(self, rws, dest):
        self._rws=rws
        self._dest=self.buildKey(dest)
        self._shortkey=self.buildShortKey(self._dest)
        self._rpc=None

    def dest(self):
        return self._dest

    def jsonEncode(self, obj):
        return self._rws.jsonEncode(obj)

    def buildKey(self, key):
        if re.match('^nd_[a-zA-Z0-9]+_[a-zA-Z0-9]+$', key):
            return key

        if re.match('^[a-zA-Z0-9]+_[a-zA-Z0-9]+$', key):
            return 'nd_{0}'.format(key)

        if re.match('^[a-zA-Z0-9]+$', key):
            return 'nd_{0}_1'.format(key)

        raise NameError(key)
        return None

    def key(self):
        return self._dest

    def buildShortKey(self, key):
        m=re.match('^nd_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)$', key)
        if m:
            return '{0}'.format(m.group(1))
        raise NameError(key)
        return None

    def __getitem__(self, key):
        if key:
            return self.node(key)
        return KeyError()

    def __getattr__(self, name):
        try:
            return self[name]
        except:
            pass
        raise AttributeError

    def discover(self):
        items=self.browse()
        for item in items:
            try:
                setattr(self, item, self[item])
            except:
                pass

    def buildNodeKey(self, key):
        # if re.match('^s_[a-zA-Z0-9]+_[a-zA-Z0-9]+$', key):
        #    return key

        if re.match('^s_.*$', key):
            return key

        return 's_{0}_{1}'.format(self._shortkey, key)

        raise NameError(key)
        return None

    def node(self, key):
        key=self.buildNodeKey(key)
        return self._rws.node(key)

    def browse(self, keyFilter=None):
        params={'dest': self.dest(), 'query': 'list/task'}
        nodes=[]
        try:
            for n in self._rws.processRequestWithContext('dcf', params).json():
                nodes.append(n['key'])
        except:
            pass

        try:
            if keyFilter:
                regex=re.compile(keyFilter)

                def myfilter(key):
                    if regex.match(key):
                        return True
                nodes=list(filter(myfilter, nodes))
        except:
            pass
        return nodes

    def browseSpecial(self, flags='', select=None):
        if select is None:
            select='key,fv,unit,flags,label'
        params={'dest': self.dest(), 'query': 'query/special'}
        data={'flags': flags, 'language': 0, 'select': select}
        try:
            return self._rws.processRequestWithContext('dcf', params, self.jsonEncode(data)).json()['r']
        except:
            pass

    def browseAlarms(self, select=None):
        return self.browseSpecial('a', select)

    def browseWarnings(self, select=None):
        return self.browseSpecial('w', select)

    def addAllNodes(self, keyFilter=None):
        nodes=self.browse(keyFilter)
        try:
            for key in nodes:
                nodes=self.node(key)
        except:
            pass

    def rpc(self):
        if self._rpc:
            return self._rpc
        self._rpc=RWSRpcMethod(self._rws, self._dest)
        return self._rpc


class RWSNode:
    def __init__(self, rws, dest):
        self._rws=rws
        self._dest=self.buildKey(dest)
        self._destProxy=None
        self._shortkey=self.buildShortKey(self._dest)
        self._items={}
        self._poller=RWSItemCollection(rws)
        self._lock=threading.Lock()
        self._rpc=None

    def dest(self):
        if self._destProxy:
            return self._destProxy
        return self._dest

    def setDestProxy(self, proxy):
        self._destProxy=proxy

    def enableVpnProxy(self, enable=True):
        if enable:
            return self.setDestProxy('s_DMZDCF_vpn')
        return self.setDestProxy(None)

    def jsonEncode(self, obj):
        return self._rws.jsonEncode(obj)

    def buildKey(self, key):
        if re.match('^s_[a-zA-Z0-9]+_[a-zA-Z0-9]+$', key):
            return key

        if re.match('^[a-zA-Z0-9]+_[a-zA-Z0-9]+$', key):
            return 's_{0}'.format(key)

        raise NameError(key)
        return None

    def key(self):
        return self._dest

    def buildShortKey(self, key):
        m=re.match('^s_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)$', key)
        if m:
            return '{0}_{1}'.format(m.group(1), m.group(2))
        raise NameError(key)
        return None

    def indexFromDotIndex(self, str):
        m=re.match('^([0-9]+)\.([0-9]+)$', str)
        if m:
            return int(m.group(1)) << 8 | int(m.group(2))
        m=re.match('^([0-9]+)$', str)
        if m:
            return int(m.group(1))
        return 0

    def buildItemKey(self, key):
        if re.match('^r_{0}_[@a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+$'.format(self._shortkey), key):
            return key
        m=re.match('^[a-zA-Z0-9]+_[@a-zA-Z0-9]+_[a-zA-Z0-9]+$', key)
        if m:
            return 'r_{0}_{1}'.format(self._shortkey, key)

        m=re.match('^[@a-zA-Z0-9]+_[a-zA-Z0-9]+$', key)
        if m:
            return 'r_{0}_{1}_0'.format(self._shortkey, key)

        m=re.match('^([@a-zA-Z]+)([0-9]+)$', key)
        if m:
            return 'r_{0}_{1}_{2}_0'.format(self._shortkey, m.group(1), m.group(2))

        m=re.match('^[aAdD][iIoO]([0-9]+\.[0-9]+)$', key)
        if m:
            index=self.indexFromDotIndex(m.group(1))
            return 'r_{0}_cio_{1}_0'.format(self._shortkey, index)

        m=re.match('^[aAdD][iIoO]([0-9]+\.[0-9]+)p$', key)
        if m:
            index=self.indexFromDotIndex(m.group(1))
            return 'r_{0}_ciop_{1}_0'.format(self._shortkey, index)

        m=re.match('^[aAdD][iIoO]([0-9]+\.[0-9]+)t$', key)
        if m:
            index=self.indexFromDotIndex(m.group(1))
            return 'r_{0}_ciot_{1}_0'.format(self._shortkey, index)

        m=re.match('^[a-zA-Z0-9]+$', key)
        if m:
            return 'r_{0}_{1}_0_0'.format(self._shortkey, key)

        raise NameError(key)
        return None

    def __getitem__(self, key):
        if key:
            return self.item(key)
        return KeyError()

    def __getattr__(self, name):
        try:
            return self[name]
        except:
            pass
        raise AttributeError

    def discover(self):
        items=self.browse()
        for item in items:
            try:
                setattr(self, item, self[item])
            except:
                pass

    def item(self, key):
        key=self.buildItemKey(key)
        if key in self._items:
            return self._items[key]

        item=RWSNodeItem(self, key)

        self._items[item.key()]=item
        self._poller.addItem(item)
        return item

    def items(self):
        return self._items

    def onlineItem(self):
        return self.item('r_{0}_@on_0_0'.format(self._shortkey))

    def isOnline(self):
        item=self.onlineItem()
        item.readState()
        if item.state():
            return True
        return False

    def addItem(self, key):
        return self.item(key)

    def addItems(self, keys):
        for key in keys:
            self.addItem(key)

    def browse(self, keyFilter=None):
        params={'dest': self.dest(), 'query': 'list/item'}
        items=self._rws.processRequestWithContext('dcf', params).json()
        try:
            if keyFilter:
                regex=re.compile(keyFilter)

                def myfilter(key):
                    if regex.match(key):
                        return True
                items=list(filter(myfilter, items))
        except:
            pass
        return items

    def addAllItems(self, keyFilter=None):
        items=self.browse(keyFilter)
        try:
            for key in items:
                self.item(key)
        except:
            pass

    def readAllState(self):
        params={'dest': self.dest(), 'query': 'read/state/{0}'.format(','.join(self._items))}
        return self._rws.processRequestWithContext('dcf', params).json()

    def poll(self):
        return self._poller.poll()

    def startPoll(self):
        return self._poller.startPoll()

    def endPoll(self):
        return self._poller.endPoll()

    def rpc(self):
        if self._rpc:
            return self._rpc
        self._rpc=RWSRpcMethod(self._rws, self._dest)
        return self._rpc


class RWSRecordIterator:
    def __init__(self, container):
        self._container=container
        self._index=0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index>=len(self._container):
            raise StopIteration
        # data content generated by container (RWSRecords or RWSRecordsView)
        data=self._container[self._index]
        self._index+=1
        return data


class RWSRecords:
    def __init__(self, item):
        self._item=item
        self._x=[]
        self._y=[]
        self._flags=[]
        self._label=None
        self._unit=0xFF
        self.__load()

    def __iter__(self):
        return RWSRecordIterator(self)

    def __len__(self):
        return len(self._x)

    def __getitem__(self, item):
        return {'x': self._x[item], 'y': self._y[item], 'flags': self._flags[item]}

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def flags(self):
        return self._flags

    @property
    def key(self):
        return self._item.key()

    @property
    def label(self):
        return self._label

    @property
    def unit(self):
        return self._unit

    def str2stamp(self, str):
        m=re.match('^([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})$', str)
        if m:
            return datetime.datetime(int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)))
        return 0

    def __load(self):
        data={}
        data=self._item.jsonEncode(data)
        params={'dest': self._item._node.dest(), 'query': 'query/record/{0}'.format(self._item.key())}
        response=self._item._node._rws.processRequestWithContext('dcf', params, data).json()
        try:
            metadata=response['metadata']
            self._label=metadata['description']
            self._unit=metadata['unit']
            data=response['rows']
            for r in data:
                self._x.append(self.str2stamp(r[0]))
                self._y.append(r[2])
                self._flags.append(r[1])
        except:
            pass
        return len(self)

    def view(self):
        return RWSRecordsView(self)

    def gwsheet(self, sheet, aref='a1'):
        try:
            sheet.vwrite(self.x, aref)
            sheet.vwrite(self.y, sheet.right(aref, 1))
            sheet.vwrite(self.flags, sheet.right(aref, 2))
            sheet.update()
        except:
            pass


class RWSRecordsView:
    def __init__(self, records):
        self._records=records
        self._filters=[]
        self._x=[]
        self._y=[]
        self._valid=False

    def __iter__(self):
        self.refresh()
        return RWSRecordIterator(self)

    def __len__(self):
        self.refresh()
        return len(self._x)

    def __getitem__(self, item):
        self.refresh()
        return {'x': self._x[item], 'y': self._y[item]}

    def invalidate(self):
        self._valid=False

    def addFilter(self, f):
        self._filters.append(f)
        self.invalidate()

    def dt(self, doffset=0, hoffset=0, moffset=0):
        delta=self.dtoffset(doffset, hoffset, moffset)
        return datetime.datetime.now()+delta

    def dtoffset(self, doffset=0, hoffset=0, moffset=0):
        return datetime.timedelta(doffset, hoffset, moffset)

    def filterFrom(self, dt):
        return self.addFilter(lambda r: r['x']>=dt)

    def filterTo(self, dt):
        return self.addFilter(lambda r: r['x']<=dt)

    def filterMatch(self, record):
        for f in self._filters:
            if not f(record):
                return False
        return True

    def refresh(self):
        if not self._valid:
            for r in self._records:
                if self.filterMatch(r):
                    self._x.append(r['x'])
                    self._y.append(r['y'])
            self._valid=True

    def x(self):
        self.refresh()
        return self._x

    def y(self):
        self.refresh()
        return self._y


class RWSNodeItem:
    def __init__(self, node, key):
        self._node=node
        self.onUpdate=Event()
        self._key=key
        self._data={}
        self._labels={}
        self._lock=threading.Lock()
        self._rpc=None

    def jsonEncode(self, obj):
        return self._node.jsonEncode(obj)

    def key(self):
        return self._key

    def keyPart(self, part):
        return self._node._rws.keyPart(self.key(), part)

    def node(self):
        return self._node

    def compareData(self, data):
        try:
            if data['value'] != self._data['value']:
                return False
            if data['unit'] != self._data['unit']:
                return False
            if data['flags'] != self._data['flags']:
                return False
        except:
            return False
        return True

    def setData(self, data):
        try:
            updated=not self.compareData(data)
            if updated:
                self._data=data
                self.onUpdate.fire(self, 'onUpdate')
        except:
            pass

    def poll(self):
        return self.readState()

    def readLabels(self, refresh=False):
        if refresh or not self._labels:
            b=self._node._rws.browser()
            labels=b.searchLabelsFromKey(self.key())
            if labels:
                self._labels=labels
        return self._labels

    def tag(self):
        labels=self.readLabels()
        try:
            return labels['name']
        except:
            pass

    def label(self):
        labels=self.readLabels()
        try:
            return labels['label']
        except:
            pass

    def readState(self):
        params={'dest': self._node.dest(), 'query': 'read/state/{0}'.format(self.key())}
        self.setData(self._node._rws.processRequestWithContext('dcf', params).json())
        return self._data

    def updateState(self, value, flags=None):
        # data={'value':value}
        # if flags != None:
        #    data['flags']=flags

        # Note: data must be passed in GET, not POST
        # data=self.jsonEncode(data)
        params={'dest': self._node.dest(), 'query': 'update/state/{0}'.format(self.key()), 'data': value}
        return self._node._rws.processRequestWithContext('dcf', params).success()

    def image(self):
        try:
            if self._data['dt']=='image':
                data=b64decode(self.rawvalue(False))
                image=Image.open(six.BytesIO(data))
                return image
        except:
            pass
        return None

    def savepng(self, fpath):
        fpath=os.path.expanduser(fpath)
        image=self.image()
        image.save(fpath)

    def set(self, value):
        return self.updateState(value)

    def manual(self, value):
        return self.updateState(value, 0x1 << 4)

    def auto(self):
        return self.updateState(0, 0)

    def on(self):
        return self.updateState(1)

    def off(self):
        return self.updateState(0)

    def toggle(self):
        return self.updateState(2)

    def blink(self, repeat=1, delay=1.0):
        while True:
            repeat-=1
            self.toggle()
            time.sleep(delay)
            self.toggle()
            if repeat<=0:
                break
            time.sleep(delay)

    def state(self):
        return bool(int(self.rawvalue(True)))

    def fvalue(self):
        return float(self.rawvalue(True))

    def rawvalue(self, refresh=True):
        if refresh:
            self.readState()
        try:
            return self._data['value']
        except:
            pass
        return 0

    @property
    def value(self):
        value=self.rawvalue(True)
        try:
            if self._data['dt']=='image':
                return self.image()
        except:
            pass
        return value

    @value.setter
    def value(self, value):
        # print "SET from property", value
        self.set(value)

    @property
    def unit(self):
        try:
            return self._data['unit']
        except:
            pass
        return None

    def unitstr(self):
        try:
            return UNIT_STR[self.unit]
        except:
            pass
        return ''

    def flags(self):
        try:
            return int(self._data['flags'])
        except:
            return 0

    def isManual(self):
        return bool(self.flags() & (0x1 << 4))

    def isAuto(self):
        return not self.isManual() and not self.isDerogation()

    def records(self):
        return RWSRecords(self)

    def rpc(self):
        if self._rpc:
            return self._rpc
        self._rpc=RWSRpcMethod(self._node._rws, self._node._dest, self._key)
        return self._rpc


class RWSItemCollection:
    def __init__(self, rws):
        self._items={}
        self._rws=rws
        self._idPoll=0
        self._refresher=None
        self._manager=RWSThread(self.pollManager)

    def __del__(self):
        self.dispose()

    def dispose(self):
        self._manager.stop()

    def addItem(self, item):
        self._idPoll=0
        return self._items.setdefault(item.key(), item)

    def registerPoll(self, pollTime=15, language='FR'):
        self._idPoll=0
        if len(self._items)>0:
            keys=','.join(list(self._items.keys()))
            params={'pollTime': pollTime, 'language': language, 'varKeys': keys}
            self._idPoll=self._rws.processRequestWithContext('OpenDcf', params).attr('serviceId')
        return self._idPoll

    def unregisterPoll(self):
        if self._idPoll:
            params={'serviceId': self._idPoll}
            self._idPoll=0
            self._rws.processRequestWithContext('CloseDcf', params)

    def poll(self):
        if not self._idPoll:
            self.registerPoll()

        if self._idPoll:
            params={'serviceId': self._idPoll}
            response=self._rws.processRequestWithContext('pollDcf', params)
            if response.success():
                try:
                    for i in response.json():
                        try:
                            idata=i['VariableState']
                            key=idata['key']
                            self._items[key].setData(idata)
                            # print self._items[key].fvalue()
                        except:
                            pass
                except:
                    pass
            elif response.error()==7:
                self._idPoll=0

    def startPoll(self):
        self._manager.start()

    def endPoll(self, waitTimeout=0):
        self._manager.stop()
        if waitTimeout>0:
            self._manager.join(waitTimeout)

    def pollManager(self):
        while not self._manager.isStop():
            self.poll()
            time.sleep(1)


class RWSRpcHandler:
    def __init__(self, rpc, name, description=None, prototype=None):
        self._rpc=rpc
        self._name=name
        self._cid=self._name.lower()
        self._description=description
        self._prototype=prototype

    def __call__(self, **kwargs):
        return self.invoke(**kwargs)

    def cid(self):
        return self._cid

    def name(self):
        return self._name

    def description(self):
        return self._description

    def prototype(self):
        return self._prototype

    def signature(self):
        print((json.dumps(self.prototype(), sort_keys=True, indent=2, separators=(',', ': '))))

    def invoke(self, **kwargs):
        params={'dest': self._rpc._dest, 'query': self._rpc.getAction('call')}
        data={'name': self._name}
        if kwargs:
            args={}
            for k, v in list(kwargs.items()):
                args[k]=v
            data['parameters']=args
        data=self._rpc._rws.jsonEncode(data)
        response=self._rpc._rws.processRequestWithContext('dcf', params, data).json()
        if response:
            return response
        return None


class RWSRpc:
    def __init__(self, rws, rpcType, dest, key=None):
        self._rws=rws
        self._rpcType=rpcType
        self._dest=dest
        self._key=key
        self._handlers={}
        self.reload()

    def reload(self):
        self._handlers={}
        params={'dest': self._dest, 'query': self.getAction('list')}
        response=self._rws.processRequestWithContext('dcf', params).json()
        if response:
            try:
                for c in response['data']:
                    self.addHandler(c['name'], c['description'], c)
            except:
                pass

    def getHandler(self, name):
        try:
            return self._handlers[name.lower()]
        except:
            return None

    def addHandler(self, name, description=None, prototype=None):
        handler=self.getHandler(name)
        if  not handler:
            handler=RWSRpcHandler(self, name, description, prototype)
            self._handlers[handler.cid()]=handler
            setattr(self, name, handler)
        return handler

    def getAction(self, query):
        action='{0}/{1}'.format(query, self._rpcType)
        if self._key:
            action += '/{0}'.format(self._key)
        return action

    def browse(self):
        handlers=[]
        for handler in list(self._handlers.values()):
            handlers.append(handler.name())
        return handlers

    # def invoke(self, name, **kwargs):
    #   handler=self.getHandler(name)
    #   if handler:
    #       return handler.invoke(**kwargs)
    #   return None


class RWSRpcMethod(RWSRpc):
    def __init__(self, rws, dest, key=None):
        RWSRpc.__init__(self, rws, 'method', dest, key)


class RWSRpcCommand(RWSRpc):
    pass


class RWSThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        self.eventStop=threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        self.eventStop.reset()
        self._target(*self._args)

    def stop(self):
        self.eventStop.set()

    def isStop(self):
        return self.eventStop.isSet()


if __name__ == "__main__":
    pass
