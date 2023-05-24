import evfl
import os
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re

FPS = 30
fileName = ""
workPlaceRoot = "cache"
streamsRoot = r"D:\game\switch\The Legend of Zelda Tears of the Kingdom\nca_dump\1\Voice\Resource\JPja\EventFlowMsg"
vgmstream = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"
bfevflRoot = "cache"
movieRoot = r"D:\game\switch\The Legend of Zelda Tears of the Kingdom\nca_dump\1\Event\Movie"

bfevflRoot = r"D:\game\dump_totk_files\000-workplace\cache"
msgRoot = r"D:\game\dump_totk_files\000-workplace\CNzh.Product.100\EventFlowMsg"

cgBgmRoot = r'D:\game\switch\The Legend of Zelda Tears of the Kingdom\temp_nca\1\Sound\Resource\Stream'

timeFormat = r'%H:%M:%S,%f'
zeroTimeFormat = '00:00:00,000'


def progressWebm(fileName, allMsg):
  # message = getMessage(fileName.replace("_PreRender.webm",""))
  clipsData,timeLineLength = getEnventFlow(fileName.replace(".webm",".bfevfl"))
  counter = 0
  baseWavName = os.path.join(workPlaceRoot, "slience_{}.wav".format(counter % 2))
  outputWavName = os.path.join(workPlaceRoot, "slience_{}.wav".format(counter % 2 + 1))
  genSlienctWav(baseWavName, timeLineLength / FPS)
  subTitles = []
  # attach voice line to slient wav
  # startTime = datetime.strptime(zeroTimeFormat, timeFormat)
  # endTime = datetime.strptime(zeroTimeFormat, timeFormat)
  for clipData in clipsData:
    # ! manually offset
    clipData['startFrame'] += 10
    voiceName = clipData["MessageId"].split(":")[-1]
    bwav = voiceName + ".bwav"
    wav = voiceName + ".wav"

    baseWavName = os.path.join(workPlaceRoot, "slience_{}.wav".format(counter % 2))
    outputWavName = os.path.join(
      workPlaceRoot, "slience_{}.wav".format((counter + 1) % 2)
    )

    startTime = datetime.strptime(zeroTimeFormat, timeFormat)
    startTime += timedelta(seconds=float(clipData['startFrame'] /FPS))
    audioDuration = clipData['duration'] /FPS
    endTime = startTime + timedelta(seconds=float(audioDuration))
    startTimeStr = datetime.strftime(startTime, timeFormat)
    endTimeStr = datetime.strftime(endTime, timeFormat)

    textRefPath = clipData['MessageId'].split(':')
    textRefSource = textRefPath[0].split('/')[-1]
    textRefStreamName = textRefPath[-1]
    text = allMsg[textRefSource][textRefStreamName]
    subTitleLine = '{} --> {}\n{}\n\n'.format(startTimeStr[:-3], endTimeStr[:-3], text)
    
    subTitles.append([clipData['startFrame'] ,subTitleLine])

    shutil.copyfile(
      os.path.join(streamsRoot, textRefSource + '_Stream',bwav),
      os.path.join(workPlaceRoot, bwav),
    )
    bwav2wav(os.path.join(workPlaceRoot, voiceName))
    #
    # http://underpop.online.fr/f/ffmpeg/help/adelay.htm.gz
    # https://stackoverflow.com/questions/32949824/ffmpeg-mix-audio-at-specific-time
    # https://stackoverflow.com/questions/35509147/ffmpeg-amix-filter-volume-issue-with-inputs-of-different-duration
    os.system(
      'ffmpeg -y -i {} -i {} -filter_complex "[1]adelay={}|{}[a1];[0:a][a1]amix=inputs=2:duration=longest:normalize=0" {}'.format(
        baseWavName,
        os.path.join(workPlaceRoot, wav),
        int((clipData["startFrame"] / FPS) * 1000),
        int((clipData["startFrame"] / FPS) * 1000),
        outputWavName,
      )
    )
    counter += 1


  #sort subtitles according start frame
  subTitles = sorted(subTitles, key=lambda x:x[0])
  subTitles  = ['{}\n{}'.format(counter, subTitles[counter][1]) for counter in range(len(subTitles))]
  with open(os.path.join(workPlaceRoot, 'output', fileName.replace('.webm','') + '.srt') , 'w+',encoding='utf8') as subTitleFile:
    subTitleFile.writelines(subTitles)

  # mix voice and bgm
  cgBgmBwavName = fileName.replace("_PreRender.webm",".bwav")
  cgBgmWavName = fileName.replace("_PreRender.webm",".wav")
  shutil.copyfile(
  os.path.join(cgBgmRoot, cgBgmBwavName),
  os.path.join(workPlaceRoot, cgBgmBwavName),
  )
  bwav2wav(os.path.join(workPlaceRoot, cgBgmBwavName.replace('.bwav','')),)
  os.system(
  'ffmpeg -y -i {} -i {} -filter_complex "[1]adelay={}[a1];[0:a][a1]amix=inputs=2:duration=longest:normalize=0" {}'.format(
    outputWavName,
    os.path.join(workPlaceRoot, cgBgmWavName),
   0,
    os.path.join(workPlaceRoot, 'output', cgBgmWavName),
    )
  )
  #merge bgm and voice
  shutil.copyfile(
  os.path.join(movieRoot, fileName),
  os.path.join(workPlaceRoot, fileName),
  )
  os.system(
    'ffmpeg -y -i {} -i {} -c:v copy -c:a aac {}'.format(
      os.path.join(workPlaceRoot, fileName),
      os.path.join(workPlaceRoot, 'output', cgBgmWavName),
      os.path.join(workPlaceRoot, 'output', fileName.replace(".webm",".mp4")),
      )
    )
  print('Done for ' + fileName)



def getEnventFlow(fileName):
  flow = evfl.EventFlow()
  with open(os.path.join(bfevflRoot, fileName) , "rb") as file:
    flow.read(file.read())
    clips = flow.timeline.clips
    timeLineLength = flow.timeline.duration  # frame
    clipsData = []
    for clip in clips:
      data = clip.params.data
      if len(data) > 1 and "MessageId" in data.keys():
        # MessageId
        # print('start time: {}'.format(clip.start_time))
        if data["Speaker"] == "Player":
          continue
        data["startFrame"] = clip.start_time
        data["duration"] = clip.duration
        clipsData.append(data)
  return clipsData,timeLineLength


#https://stackoverflow.com/questions/24045892/why-does-elementtree-reject-utf-16-xml-declarations-with-encoding-incorrect
def getMessage(fileName):  
  voiceLines = {}
  with open(os.path.join(msgRoot, fileName + ".xmsbt"), 'r', encoding='utf16') as msgFile:
    # remove control character like &#xE;\0&#x4;\0
    contenet = msgFile.read()
    contenet = re.sub(r'&#x\w;\\0', '', contenet)
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
  


def genSlienctWav(filename, lengthSeconds):
  os.system(  
    "ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=mono -t {} -acodec pcm_s16le {}".format(
      lengthSeconds, filename
    )
  )


def bwav2wav(filePathNoExtension):
  os.system(
    "{} {}.bwav -o {}.wav".format(
      vgmstream, filePathNoExtension, filePathNoExtension
    )
  )
  pass





if __name__ == "__main__":
  
  # targets = os.listdir(movieRoot)
  os.makedirs(os.path.join(workPlaceRoot, 'output',), exist_ok=True, mode=0o777)
  # 2 of them have no text, just merge wav and webm
  targets = [
    "DmT_OP_GanonWakeUp_PreRender.webm",
    "DmT_SY_BloodyMoonDarkZelda_PreRender.webm",
    "DmT_SY_BloodyMoonFirst_PreRender.webm",
    # "DmT_SY_BloodyMoon_PreRender.webm",
    "DmT_ZE_Birth_PreRender.webm",
    "DmT_ZE_LieServant_PreRender.webm",
    "DmT_ZE_Meet_PreRender.webm",
    "DmT_ZE_Molduga_PreRender.webm",
    "DmT_ZE_QueenDead_PreRender.webm",
    "Dm_BC_0012_PreRender.webm",
    "Dm_BZ_0005_PreRender.webm",
    "Dm_ED_0007_PreRender.webm",
    "Dm_GE_0025_PreRender.webm",
    "Dm_GO_0021_PreRender.webm",
    "Dm_OT_0015_PreRender.webm",
    "Dm_RT_0022_PreRender.webm",
    "Dm_SK_0003_PreRender.webm",
    "Dm_ZE_0004_PreRender.webm",
    "Dm_ZE_0005_PreRender.webm",
    "Dm_ZE_0006_PreRender.webm",
    "Dm_ZE_0007_PreRender.webm",
    "Dm_ZE_0008_PreRender.webm",
    "Dm_ZE_0010_PreRender.webm",
    "Dm_ZE_0011_PreRender.webm",
    "Dm_ZN_0033_PreRender.webm",
    "Dm_ZN_0039_PreRender.webm",
    # "Dm_ZN_0069_PreRender.webm",
    "Dm_ZO_0032_PreRender.webm",
  ]

  extraText = [
    'Dm_ZN_0032'
  ]

  allMsg = {}
  for webm in targets + extraText:
    # Dm_BZ_0005_PreRender.webm ref DmT_ZE_Birth.xmsbt
    filenameOnly = webm.replace("_PreRender.webm","")
    allMsg[filenameOnly] = getMessage(filenameOnly)
  #DEBUG
  # targets = ['DmT_OP_GanonWakeUp_PreRender.webm']
  for webm in targets:
    progressWebm(webm, allMsg)
print("DONE")
