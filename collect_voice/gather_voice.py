import json
import os
import shutil
import xml.etree.ElementTree as ET
import re

streamsRoot = r"D:\game\switch\The_Legend_of_Zelda_Tears_of_the_Kingdom\nca_dump\1\Voice\Resource\JPja\EventFlowMsg"
msgRoot = r"D:\game\dump_totk_files\000-workplace\CNzh.Product.100\EventFlowMsg"
workPlaceRoot = "cache"
vgmstream = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"


def bwav2wav(filePathNoExtension):
    os.system(
        "{} {}.bwav -o {}.wav".format(
            vgmstream, filePathNoExtension, filePathNoExtension
        )
    )


def getMessage(fileName):  
  voiceLines = {}
  with open(os.path.join(msgRoot, fileName + ".xmsbt"), 'r', encoding='utf16') as msgFile:
    # remove control character like &#xE;\0&#x4;\0
    contenet = msgFile.read()
    contenet = re.sub(r'&(#)?\w+;((Z)?\\0|\}|ć|Ā|ā|Ĉ|Č|ċ)?', '', contenet)
    root = ET.fromstring(contenet)
    entries = [child for child in root]
    for entry in entries:
      for child in entry:
        if(child.text != None):
          # if(len(child.text) > 0):
          voiceLines[entry.attrib['label']] = child.text
        else:
          voiceLines[entry.attrib['label']] = ''
  return voiceLines



allMsg = {}
for fileName in os.listdir(msgRoot):
    if(fileName.endswith('.xmsbt')):
        fileName = fileName.replace('.xmsbt','')
        allMsg[fileName] = getMessage(fileName)

with open('./allMsg.json','w+',encoding='utf8') as file:
    file.write(json.dumps(allMsg,ensure_ascii=False))




clipsData = []
with open("./allclipsData.json", "r") as file:
    clipsData = json.loads(file.read())

flatendData = []
for data in clipsData:
    flatendData += data
textMap = {}
# TODO search unuse voice
for clip in flatendData:
    messageId = clip["MessageId"]
    folderName, streamName = messageId.split("/")[1].split(":")
    speaker = clip["Speaker"]
    bwav = streamName + ".bwav"
    wav = streamName + ".wav"
    speakerRoot= os.path.join(workPlaceRoot, speaker)
    if(not os.path.exists(path=speakerRoot)):
        os.mkdir(speakerRoot)
    if(not speaker in textMap.keys()):
       textMap[speaker] = {}
    #search text
    try:
        textMap[speaker][streamName] = allMsg[folderName][streamName]
    except KeyError as e:
       textMap[speaker][streamName] = ""

    # shutil.copyfile(
    #     os.path.join(streamsRoot, folderName + "_Stream", bwav),
    #     os.path.join(workPlaceRoot, bwav),
    # )
    # bwav2wav(os.path.join(workPlaceRoot, streamName))
    # shutil.move(
    #     os.path.join(workPlaceRoot, wav),
    #     os.path.join(workPlaceRoot, speaker, wav),
    # )

with open('./textMap.json','w+',encoding='utf8') as file:
    file.write(json.dumps(textMap,ensure_ascii=False))
print("DONE")
