import re, random
from PMS import *

##################################################################################################
FX_PLUGIN_PREFIX     = "/video/Fx"

FX_URL                     = "http://www.fxnetworks.com"
FX_FULL_EPISODES_SHOW_LIST = "http://www.fxnetworks.com/episodes.php"
CACHE_INTERVAL             = 3600
DEBUG                      = False
fxart                      ="art-default.jpg"
fxthumb                    ="icon-default.jpg"
####################################################################################################

def Start():
  Plugin.AddPrefixHandler(FX_PLUGIN_PREFIX, MainMenu, "Fx","icon-default.jpg", "art-default.jpg")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
  
  MediaContainer.art        =R(fxart)
  DirectoryItem.thumb       =R(fxthumb)
  WebVideoItem.thumb= R(fxthumb)

####################################################################################################
#def MainMenu():
#    dir = MediaContainer(mediaType='video') 
#    dir.Append(Function(DirectoryItem(all_shows, "All Shows"), pageUrl = FX_FULL_EPISODES_SHOW_LIST))
    
   
#    return dir
    
####################################################################################################
def MainMenu():
    dir = MediaContainer(mediaType='video')
    pageUrl=FX_FULL_EPISODES_SHOW_LIST
    content = XML.ElementFromURL(pageUrl, True)
    for item in content.xpath('//div[@id="episodes"]//div/ul/li'):
      titleUrl=item.xpath("a")[0].get('href')
      Log(titleUrl)
      if titleUrl.count('/watch/') !=0:
        titleUrl=titleUrl.replace('/watch','/fod') + "/rss.xml"
      title = item.xpath("a")[0].text_content().strip()
      Log(titleUrl)
      dir.Append(Function(DirectoryItem(VideoPage, title), pageUrl = titleUrl))
    return dir 

####################################################################################################
def VideoPage(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    Log("Hello")
    Log(pageUrl)
    content = XML.ElementFromURL(pageUrl, False)
    for item2 in content.xpath('/rss/channel/item'):


      vidUrl=item2.xpath("link")[0].text
      Log(vidUrl)
      title2 = item2.xpath("title")[0].text
      
      
      
      content2 = XML.ElementFromURL(vidUrl,True)
      pageUrl2=pageUrl.replace("/rss.xml","")
      pagUrl2=pageUrl.replace("fod//","fod/")
      pageUrl2=pageUrl2.replace("/","%2F")
      pageUrl2=pageUrl2.replace(":","%3A")
      pageUrl2=pageUrl2+"&%40"
      

      videoID = content2.xpath('//div[@id="player"]//object/param[@name="@videoPlayer"]')[0].get("value")
      bgcolor = content2.xpath('//div[@id="player"]//object/param[@name="bgcolor"]')[0].get("value")
      bgcolor=bgcolor.replace("#","%23")
      width = content2.xpath('//div[@id="player"]//object/param[@name="width"]')[0].get("value")
      height = content2.xpath('//div[@id="player"]//object/param[@name="height"]')[0].get("value")
      playerID = content2.xpath('//div[@id="player"]//object/param[@name="playerID"]')[0].get("value")
      publisherID = content2.xpath('//div[@id="player"]//object/param[@name="publisherID"]')[0].get("value")
      isVid = content2.xpath('//div[@id="player"]//object/param[@name="isVid"]')[0].get("value")
      videoPlayer = content2.xpath('//div[@id="player"]//object/param[@name="@videoPlayer"]')[0].get("value")
      wmode = content2.xpath('//div[@id="player"]//object/param[@name="wmode"]')[0].get("value")
      adServerURL = content2.xpath('//div[@id="player"]//object/param[@name="adServerURL"]')[0].get("value")
      showCode = content2.xpath('//div[@id="player"]//object/param[@name="showCode"]')[0].get("value")
      omnitureAccountID = content2.xpath('//div[@id="player"]//object/param[@name="omnitureAccountID"]')[0].get("value")
      dynamicStreaming = content2.xpath('//div[@id="player"]//object/param[@name="dynamicStreaming"]')[0].get("value")
      optimizedContentLoad = content2.xpath('//div[@id="player"]//object/param[@name="optimizedContentLoad"]')[0].get("value")
      convivaEnabled = content2.xpath('//div[@id="player"]//object/param[@name="convivaEnabled"]')[0].get("value")
      convivaID = content2.xpath('//div[@id="player"]//object/param[@name="convivaID"]')[0].get("value")
      

      
      truevidUrl="http://admin.brightcove.com/viewer/us1.24.00.06a/BrightcoveBootloader.swf?purl=" + pageUrl2 + "videoPlayer=" + videoID + "&adServerURL=" + adServerURL + "&autoStart=true" + "&bgcolor=" + bgcolor + "&convivaEnabled=" + convivaEnabled + "&convivaID=" + convivaID + "&dynamicStreaming=" + dynamicStreaming + "&flashID=myExperience" + "&height=" + height + "&isVid=" + isVid + "&omnitureAccountID=" + omnitureAccountID + "&optimizedContentLoad=" + optimizedContentLoad + "&playerID=" + playerID + "&publisherID=" + publisherID + "&showcode=" + showCode + "&width=" + width +"&wmode=" + wmode
      
      Log(truevidUrl)

      dir.Append(WebVideoItem(truevidUrl, title=title2))
    return dir
