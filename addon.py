#
#    Dette program er udviklet af Tim H. Nielsen
#    Der er fundet inspiration og taget udgangspunkt i et eksempel fra Tommy Winthers, videovideo, plugin.
#    Scriptet benytter JSON.
#    Credits - http://tommy.winther.nu/wordpress/
#    2012 (C) - THN
#
#    This Program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2, or (at your option)
#    any later version.
#
#    This Program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this Program; see the file LICENSE.txt. If not, write to
#    the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#    http://www.gnu.org/copyleft/gpl.html
#
import xbmcgui
import sys
import xbmcplugin
import xbmcaddon
from urlparse import parse_qs, urlparse
import urllib2
import json
import os

# Thank You!
# http://www.pythonforbeginners.com/code-snippets-source-code/using-the-youtube-api/
#

# thank you!
# https://github.com/skystrife/xbmc-plugin-mpdc/commit/37dbdd9c26553960c6403566da762ced92a7e5e8
#

YJSON = 'http://gdata.youtube.com/feeds/api/users/LivingSmartTV/uploads?alt=jsonc&v=2'
#VIMEO_VIDEO_URL = "http://vimeo.com/thewedmores/videos/rss"

class LSTVHD(object):
    def showOverview(self):
        try:
            ICON = os.path.join(ADDON.getAddonInfo('path'), 'icon.png')
            resp = urllib2.urlopen(YJSON)
            items = list()
            data = json.load(resp)
            #ok = xbmcgui.Dialog().yesno("Sporgsmaal","Bruger du KODI?")
            #print ok
            for item in data['data']['items']:
                title = unicode(item['title'])
                published = unicode(item['uploaded'])
                description = unicode(item['description'])
                jDuration = unicode(item['duration'])
                jPlayer_url = item['player']['default']
                jThumbnail_url = item['thumbnail']['hqDefault']
                item = xbmcgui.ListItem(title.encode('utf-8'), iconImage = unicode(ICON).encode('utf-8'), thumbnailImage = title.encode('utf-8') )
                infoLabels = {
                    'title' : title,
                    'plot' : description,
                    'published' : published,
                    'duration' : jDuration
                }
                item.setInfo('video', infoLabels)
                item.setProperty("IsPlayable","true")
                item.setProperty('Fanart_Image', jThumbnail_url)
                xbmc_youtube_id =  parse_qs(urlparse(unicode(jPlayer_url)).query)['v'][0];
                xbmc_url = PATH % xbmc_youtube_id
                xbmcplugin.addDirectoryItem(HANDLE, xbmc_url, item, False)
                items.append((xbmc_url, item, False))
            xbmcplugin.addDirectoryItems(HANDLE,items)
            xbmcplugin.endOfDirectory(HANDLE)
        except Exception:
            self.message(ADDON.getLocalizedString(30900))
    def message(self, message):
        dialog = xbmcgui.Dialog()
        line1 = ADDON.getLocalizedString(99990)
        line2 = ADDON.getLocalizedString(99991)
        error = ADDON.getLocalizedString(99992)
        dialog.ok(message, line1, line2, error)
if __name__ == '__main__':
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    #FANART_IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'fanart.jpg')
    PATH = 'plugin://plugin.video.youtube/?path=/root/search/new&action=play_video&videoid=%s'
   # VIMEO_PATH = 'plugin://plugin.video.vimeo/?path=/root/subscriptions/new&action=play_video&videoid=%s'
    HANDLE = int(sys.argv[1])
    lstv = LSTVHD()
    lstv.showOverview()
