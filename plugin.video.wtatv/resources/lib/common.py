# -*- coding: utf-8 -*-

import json,os,re,sys,urllib,urlparse
import time,datetime
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import uuid
from hashlib import md5

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()
addon_id = addon.getAddonInfo('id')
addon_name = addon.getAddonInfo('name')
version = addon.getAddonInfo('version')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
content = addon.getSetting('content')
view_id = addon.getSetting('view_id')
force_view = addon.getSetting('force_view') == 'true'
cookie = addon.getSetting('cookie')

base_url = 'http://www.wtatv.com'

time_format = '%Y-%m-%d %H:%M:%S'

def log(msg):
    xbmc.log(str(msg), xbmc.LOGNOTICE)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)
    
def utfenc(str):
    try:
        str = str.encode('utf-8')
    except:
        pass
    return str
    
def getString(id):
    return addon.getLocalizedString(id)

def time_stamp(str_date):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(str_date,time_format)))

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def utc2local(date_string):
    if date_string:
        utc = datetime.datetime(*(time.strptime(date_string, time_format)[0:6]))
        epoch = time.mktime(utc.timetuple())
        offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
        return (utc + offset).strftime(time_format)

def uniq_id(t=1):
    mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    if not ":" in mac_addr: mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    # hack response busy
    i = 0
    while not ":" in mac_addr and i < 3:
        i += 1
        time.sleep(t)
        mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    if ":" in mac_addr and t == 1:
        device_id = str(uuid.UUID(md5(str(mac_addr.decode("utf-8"))).hexdigest()))
        addon.setSetting('device_id', device_id)
        return True
    elif ":" in mac_addr and t == 2:
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(mac_addr)).bytes
    else:
        log("[%s] error: failed to get device id (%s)" % (addon_id, str(mac_addr)))
        dialog.ok(addon_name, getString(30051))
        return False