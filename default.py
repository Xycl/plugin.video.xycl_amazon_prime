#!/usr/bin/python
# -*- coding: utf8 -*-

""" 
Amazon Prime Instant Video
Copyright (C) 2014 Xycl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


# python imports
import urllib, urllib2, re, os
from HTMLParser import HTMLParser

# xbmc imports
import xbmcplugin, xbmcgui, xbmc


def smart_unicode(s):
    """credit : sfaxman"""
    if not s:
        return ''
    try:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'UTF-8')
        elif not isinstance(s, unicode):
            s = unicode(s, 'UTF-8')
    except:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'ISO-8859-1')
        elif not isinstance(s, unicode):
            s = unicode(s, 'ISO-8859-1')
    return s


def smart_utf8(s):
    return smart_unicode(s).encode('utf-8')

    
# not used    
def log(msg, level=xbmc.LOGDEBUG):

    if type(msg).__name__=='unicode':
        msg = msg.encode('utf-8')

    filename = smart_utf8(os.path.basename(sys._getframe(1).f_code.co_filename))
    lineno  = str(sys._getframe(1).f_lineno)

    try:
        module = "function " + sys._getframe(1).f_code.co_name
    except:
        module = " "

    xbmc.log(str("[%s] line %5d in %s %s >> %s"%("plugin.video.wdrrockpalast", int(lineno), filename, module, msg.__str__())), level)   
    

def add_dir(name, url, mode, iconimage):
    try:
        display_name = HTMLParser().unescape(smart_unicode(name))
    except:
        display_name = name
        pass

    ok=True
    liz=xbmcgui.ListItem(display_name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": display_name } )
    if mode == 1:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    else:
        u = "plugin://plugin.program.chrome.launcher/?kiosk=yes&mode=showSite&stopPlayback=yes&url=%s"%urllib.quote_plus(url) 
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok
            
    
def show_movies(page):
 
    # start page
    if page == '':
        req = urllib2.Request('http://www.amazon.de/s/ref=sr_nr_n_0?rh=n%3A3279204031%2Cn%3A!3010076031%2Cn%3A3356018031&bbn=3279204031&sort=popularity-rank&ie=UTF8&qid=1401261746&rnid=3279204031')
    # subsequent pages
    else:
        req = urllib2.Request(page)
        
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    
    # find movies
    match=re.compile('<img onload=.*?src="(.*?)" class="productImage ilc2" />.*?</div></a><h3 class="newaps">.*?<a href="(.*?)"><span class="lrg bold">(.*?)</span></a>', re.DOTALL).findall(link)

    # add movies to list
    for img,url,name in match:
        add_dir(name, url, 2, img)
            
    # find link to next page
    match=re.compile('<a title="Nächste Seite".*?id="pagnNextLink".*?class="pagnNext".*?href="(.*?)">', re.DOTALL).findall(link)
    for url in match:
        try:
            url = HTMLParser().unescape(smart_unicode(url))
        except:
            pass
        add_dir('>> Nächste Seite', 'http://www.amazon.de' + url , 1, '')
        break
    
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_params():
    """ extract params from argv[2] to make a dict (key=value) """
    param_dict = {}
    try:
        if sys.argv[2]:
            param_pairs=sys.argv[2][1:].split( "&" )
            for params_pair in param_pairs:
                param_splits = params_pair.split('=')
                if (len(param_splits))==2:
                    param_dict[urllib.unquote_plus(param_splits[0])] = urllib.unquote_plus(param_splits[1])
    except:
        pass
    return param_dict


              
params=get_params()

url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass


if mode==None or url==None or len(url)<1:
    show_movies('')
if mode == 1:
    show_movies(url)   
elif mode==2:
    play_video(url, name)


