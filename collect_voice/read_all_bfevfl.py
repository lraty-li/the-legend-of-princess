import json
import evfl
import os



fileName = ""
workPlaceRoot = "../cache"
streamsRoot = r"D:\game\switch\The Legend of Zelda Tears of the Kingdom\nca_dump\1\Voice\Resource\JPja\EventFlowMsg"
vgmstream = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"
bfevflRoot = r"D:\game\dump_totk_files\000-workplace\bfevfl"

movieRoot = r"D:\game\switch\The Legend of Zelda Tears of the Kingdom\nca_dump\1\Event\Movie"

msgRoot = r"D:\game\dump_totk_files\000-workplace\CNzh.Product.100\EventFlowMsg"


def getEnventFlow(fileName):
  flow = evfl.EventFlow()
  with open(os.path.join(bfevflRoot, fileName) , "rb") as file:
    try:
      flow.read(file.read())
      clips = flow.timeline.clips
      timeLineLength = flow.timeline.duration  # frame
    except Exception as e:
      # no clips?
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
  allclipsData = []
  for bfevfl in bfevfls:
    clipsData = getEnventFlow(bfevfl)
    if(clipsData != None and len(clipsData[0] )!=0):
      allclipsData.append(clipsData[0])
  
  with open('./allclipsData.json','w+',encoding='utf8') as file:
    file.write(json.dumps(allclipsData))
  print('DONE')