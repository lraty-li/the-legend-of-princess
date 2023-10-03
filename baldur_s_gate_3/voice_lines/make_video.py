import subprocess
import os
from datetime import datetime, timedelta
import json
import shutil
import re

# ===================================================================

# 以下编辑都要注意切换成英文输入法
# 希望生成视频的对象，这些名称来源于P5R_sound_classfied文件夹的文件夹名字，每一位以引号包住，之后以逗号分隔。
# 如果希望同时将多为对象生成为一个视频，例如武见_妙，穿朋克装的女性，为同一人，除了用引号各自包起来之外，再加多一层中括号。还是看看下面的例子吧。
speakers = [
    # "v3ed74f063c6042dc83f6f034cb47c679",
    # "v257213130c15493581769f134385451b",
    "v58a6933340bf83581d17fff240d7fb12"
]


# 希望生成的视频的图片的位置，例如回到以下路径去寻找 新岛_真.png 生成视频，支持png.jpg
imgsRoot = r"E:\modding\bd3\bd3_voices\voice_pack\Mods\Gustav\Localization\English\output"

# 解压分类好的文件后，能够看到各自语音的文件夹。
spksRoot = r"E:\modding\bd3\bd3_voices\voice_pack\Mods\Gustav\Localization\English\wavs"

# soundMapSpeaker... json文件的路径
textMapPath = r"E:\modding\bd3\bd3_voices\voice_pack\Mods\Gustav\Localization\English\voice_map.json"

# 生成的视频，字幕等的输出路径
outPutFolderRoot = r"E:\modding\bd3\bd3_voices\voice_pack\Mods\Gustav\Localization\English\output"


vgmtool = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"
ffmpeg = r"D:\.bin\ffmpeg.exe"
ffprobe = r"D:\.bin\ffprobe.exe"

# 是否将字幕文件嵌入mp4视频,False 为关闭
embedSubtitles = True

# ===================================================================

"""
import os
spksRoot = r'E:\Temp\p5r_sound_event-20230411\P5R_sound_classfied'
files = os.listdir(spksRoot)
keyword = '导航'
a = [b for b in files if keyword in b]
print(a)
"""

timeFormat = r"%H:%M:%S,%f"
zeroTimeFormat = "00:00:00,000"


def createFolder(folderPath):
    os.makedirs(folderPath, exist_ok=True, mode=0o777)


def loadJson(filePath):
    if not filePath[-5:] == ".json":
        filePath += ".json"
    with open(filePath, "r", encoding="utf8") as file:
        return json.load(file)


def gatherWavs(firstSpeakerWavsRoot, spkSrcRoot):
    wavFiles = []
    for file in os.listdir(spkSrcRoot):
        wavFiles.append(file)
        if(os.path.exists(os.path.join(firstSpeakerWavsRoot, file))):
            continue
        shutil.copyfile(
            os.path.join(spkSrcRoot, file),
            os.path.join(firstSpeakerWavsRoot, file),
        )
    return wavFiles


def lineUpAudioOfSpk(speakers, outPutFolderRoot, textMap):
    if len(speakers) == 0:
        return
    firstSpeaker = speakers[0]
    firstSpeakerRoot = os.path.join(outPutFolderRoot, firstSpeaker)
    firstSpeakerWavsRoot = os.path.join(firstSpeakerRoot, "wavs")
    createFolder(firstSpeakerWavsRoot)
    concatFileListName = os.path.join(firstSpeakerRoot, "{}.txt".format(firstSpeaker))
    outPutAudioPath = os.path.join(firstSpeakerRoot, "{}.wav".format(firstSpeaker))
    srtOutPutPath = os.path.join(firstSpeakerRoot, "{}.srt".format(firstSpeaker))
    srtLines = []
    inputAudiosFileNames = []

    wavs = []
    subTextMap = {}

    for speaker in speakers:
        spkSrcRoot = os.path.join(spksRoot, speaker)
        wavs += gatherWavs(firstSpeakerWavsRoot, spkSrcRoot)
        subTextMap.update(textMap[speaker])

    srtLines, inputAudiosFileNames = lineUpWavs(firstSpeakerWavsRoot, wavs, subTextMap)

    with open(srtOutPutPath, "w", encoding="utf8") as file:
        file.writelines(srtLines)

    with open(concatFileListName, "w", encoding="utf8") as file:
        file.writelines(inputAudiosFileNames)
    os.system(
        "ffmpeg -y -f concat -safe 0 -i {} {}".format(
            concatFileListName, outPutAudioPath
        )
    )
    # ffmpeg.input(concatFileListName, format='concat', safe=0,).output(outPutAudioPath, c='copy').run()

    vdoImg = "{}".format(os.path.join(imgsRoot, "{}.png".format(firstSpeaker)))
    if not os.path.exists(vdoImg):
        vdoImg = "{}".format(os.path.join(imgsRoot, "{}.jpg".format(firstSpeaker)))
        if not os.path.exists(vdoImg):
            vdoImg = "./img/default.png"  # default img
    outPutVdoPath = outPutAudioPath.replace(".wav", ".mp4")

    # -vf subtitles= '\\' problem
    # https://stackoverflow.com/questions/71597897/unable-to-parse-option-value-xxx-srt-as-image-size-in-ffmpeg
    # http://underpop.online.fr/f/ffmpeg/help/notes-on-filtergraph-escaping.htm.gz

    if embedSubtitles:
        os.system(
            "ffmpeg -y -loop 1 -i {0} -i {1} -vf subtitles='{2}'  -c:v libx264 -tune stillimage -c:a aac -pix_fmt yuvj420p -shortest {3}".format(
                vdoImg,
                outPutAudioPath,
                srtOutPutPath.replace("\\", "\\\\").replace(r":", r"\:"),
                outPutVdoPath,
            )
        )
    else:
        os.system(
            "ffmpeg -y -loop 1 -i {0} -i {1} -c:v libx264 -tune stillimage -c:a aac -pix_fmt yuvj420p -shortest {3}".format(
                vdoImg,
                outPutAudioPath,
                srtOutPutPath.replace("\\", "\\\\").replace(r":", r"\:"),
                outPutVdoPath,
            )
        )


def lineUpWavs(wavsRoot, wavs, textMap):
    srtLines = []
    inputAudiosFileNames = []

    startTime = datetime.strptime(zeroTimeFormat, timeFormat)
    endTime = datetime.strptime(zeroTimeFormat, timeFormat)

    counter = 1
    for sfile in wavs:
        try:
            text = textMap[re.sub(".wav", "", sfile)]
        except KeyError as e:
            # not found text
            continue
        filePath = os.path.join(wavsRoot, sfile)
        # if mono ,conver into Stereo
        sndFileChannel = countChannel(filePath)
        # if(sndFileChannel == 1):
        #     mono2stereo(filePath)
        #     pass
        if(sndFileChannel > 1):
            stereo2mono(filePath)
            pass
        
      
        audioDuration = getDurationSeconds(filePath)
        startTime = endTime
        endTime = startTime + timedelta(seconds=float(audioDuration))
        startTimeStr = datetime.strftime(startTime, timeFormat)
        endTimeStr = datetime.strftime(endTime, timeFormat)
        
        srtLine = "{}\n{} --> {}\n{}\n\n".format(
            str(counter), startTimeStr[:-3], endTimeStr[:-3], text
        )
        counter += 1
        srtLines.append(srtLine)
        inputAudiosFileNames.append("file '{}'\n".format(filePath.replace("\\", "/")))
    return srtLines, inputAudiosFileNames


def countChannel(filePath):
    # ffprobe -show_entries stream=channels -of compact=p=0:nk=1 -v 0
    command = [
        ffprobe,
        "-v",
        "fatal",
        "-show_entries",
        "stream=channels",
        "-of",
        "compact=p=0:nk=1",
        filePath,
    ]
    result = subProcessCall(command=command)
    return int(result)


def getDurationSeconds(filePath):
    # https://gist.github.com/hiwonjoon/035a1ead72a767add4b87afe03d0dd7b
    command = [
        ffprobe,
        "-v",
        "fatal",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        filePath,
    ]
    # ffmpeg.probe(filePath)["format"]["duration"]
    result = subProcessCall(command=command)
    return result


def subProcessCall(command):
    ffprobeCall = subprocess.Popen(
        command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    out, err = ffprobeCall.communicate()
    if err:
        print("error", err)
        return None
    return out

def mono2stereo(filepath):
    # ffmpeg -i .\left.wav -i .\left.wav -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map "[a]" output.wav
    monoName = filepath.replace('.wav','-mono.wav')
    shutil.move(filepath, monoName)
    command = "{} -i {} -i {} -filter_complex \"[0:a][1:a]amerge=inputs=2[a]\" -map \"[a]\" {}".format(
        ffmpeg,
        monoName,
        monoName,
        filepath
    )
    os.system(command)
    return

def stereo2mono(filepath):
    # ffmpeg -i .\left.wav -i .\left.wav -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map "[a]" output.wav
    streoName = filepath.replace('.wav','-streo16.wav')
    shutil.move(filepath, streoName)
    command = "{} -i {} -ac 1 {}".format(
        ffmpeg,
        streoName,
        filepath
    )
    os.system(command)
    return

if __name__ == "__main__":
    os.system("chcp 65001")
    textMap = loadJson(textMapPath)
    for speaker in speakers:
        if not type(speaker) == list:
            speaker = [speaker]

        lineUpAudioOfSpk(speaker, outPutFolderRoot, textMap)