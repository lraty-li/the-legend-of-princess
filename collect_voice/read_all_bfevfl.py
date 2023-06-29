import json
import evfl
import os,json



fileName = ""
workPlaceRoot = "../cache"
streamsRoot = r"D:\game\switch\The Legend of Zelda Tears of the Kingdom\nca_dump\1\Voice\Resource\JPja\EventFlowMsg"
vgmstream = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"
bfevflRoot = r"D:\Game\botw_workplace\000-workplace\bfevfl"

movieRoot = r"D:\game\switch\The Legend of Zelda Tears of the Kingdom\nca_dump\1\Event\Movie"

msgRoot = r"D:\game\dump_totk_files\000-workplace\CNzh.Product.100\EventFlowMsg"

def objPropertiesWalk(obj):
  if(obj is None):
    return
  subObjs = [obj]
  if(type(obj) is list):
      subObjs = obj
  
  for subObj in subObjs:
    try:
      properties = vars(subObj)
    except Exception as e:
      print('unknow:')
      objType = type(subObj)
      if objType in [evfl.util.Index , evfl.common.StringHolder]:
        print(subObj.v)
      elif objType is evfl.container.Container:
        print(subObj.data)
      elif objType in [evfl.common.ActorIdentifier, int]:
        print(subObj)
      else:
        print(subObj)
      return
    for prop in properties:
      # print(properties[prop])
      if(type(properties[prop]) is str):
        print(properties[prop])
      else:
        objPropertiesWalk(properties[prop]) 



def getEnventFlow(fileName):
  flow = evfl.EventFlow()
  with open(os.path.join(bfevflRoot, fileName) , "rb") as file:
    try:
      flow.read(file.read())
    # objPropertiesWalk(flow)
      clips = flow.timeline.clips
      timeLineLength = flow.timeline.duration  # frame
    except Exception as e:
      # no clips?
      print('No clips')
      return None
    clipsData = []
    for clip in clips:
      try:
        data = clip.params.data
      except Exception as e:
        #no params
        continue
      if len(data) > 1 and "MessageId" in data.keys():
        # if data["Speaker"] == "Player":
        #   continue
        data["startFrame"] = clip.start_time
        data["duration"] = clip.duration
        clipsData.append(data)
  return clipsData,timeLineLength

if __name__ == '__main__':
  bfevfls = os.listdir(bfevflRoot)
  # DEBUG
  bfevfls = ['Dm_BZ_0007.bfevfl'
             ]
  # DEBUG END
  allclipsData = []
  for bfevfl in bfevfls:
    clipsData = getEnventFlow(bfevfl)
    if(clipsData != None and len(clipsData[0] )!=0):
      allclipsData.append(clipsData[0])
  
  with open('./allclipsData.json','w+',encoding='utf8') as file:
    file.write(json.dumps(allclipsData))
  print('DONE')
