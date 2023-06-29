import os
import shutil
import json
streamsRoot = r"D:\PT\TOTK\1\Voice\Resource\USen\EventFlowMsg"
workPlaceRoot = "cache"

files = os.listdir(streamsRoot)
folders = [fold for fold in files if os.path.isdir(os.path.join(streamsRoot, fold))]

allMsg = []
with open('./allMsg.json', 'r', encoding='utf8') as file:
  allMsg = json.loads(file.read())
allMsgKeys = set(allMsg.keys())

sndMap = {}

for fold in folders:
  namePrefix = fold.split('_Stream')[0]
  if (namePrefix in allMsgKeys):
    snds = allMsg[namePrefix]
    subStreams = os.listdir(os.path.join(streamsRoot, fold))
    for subStream in subStreams:
      # shutil.copyfile(
      #     os.path.join(streamsRoot, fold, subStream),
      #     os.path.join(workPlaceRoot, subStream),
      # )
      print(subStream)
      try:
        sndMap[subStream] = snds[subStream.replace('.bwav', '')]
      except KeyError as e:
        print('not found:')
        print(subStream, snds)
with open('./sndMap.json','w+',encoding='utf8') as file:
  file.write(json.dumps(sndMap, ensure_ascii= False))

print('DONE')
