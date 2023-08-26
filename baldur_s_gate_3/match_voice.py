import xml.etree.ElementTree as ET
import json
import os
vgmstream = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"
soundBandRoot = './Soundbanks'
wavRoot = './wavs'

tree = ET.parse('./chinese.xml')
root = tree.getroot()

voiceLineMap = {}
soundMap = {}
for child in root:
    voiceLineMap[child.attrib['contentuid']] = child.text



wems = [i for i in os.listdir(soundBandRoot) if i.endswith('.wem')]

def dumpJson(path, data):
    with open(path,'w+',encoding='utf8') as file:
        file.write(json.dumps(data,ensure_ascii=False))

def wem2Wav(filePathNoExtension, inputPath, outputPath):
  os.system(
    "{} {}\{}.wem -o {}\{}.wav".format(
      vgmstream, inputPath,filePathNoExtension, outputPath,filePathNoExtension
    )
  )

def createDir(path):
    if(not os.path.exists(path)):
       os.mkdir(path)

for wem in wems:
    wemName = wem.replace('.wem','')
    wemParts = wemName.split('_')
    wemVoiceLineIndex = wemParts[-1]
    wemSpeakerIndex = wemParts[0]
    speakerRoot = os.path.join(wavRoot, wemSpeakerIndex)
    # createDir(speakerRoot)
    # wem2Wav(wemName, soundBandRoot, speakerRoot)
    try:
        soundMap[wemSpeakerIndex]
    except KeyError as e:
        soundMap[wemSpeakerIndex] = {}
    try:
        soundMap[wemSpeakerIndex][wemName] = voiceLineMap[wemVoiceLineIndex]
    except KeyError as e:
        # not found voiceLineMap[wemVoiceLineIndex]
        continue

dumpJson("./voice_lines.json", voiceLineMap)
dumpJson("./voice_map.json", soundMap)