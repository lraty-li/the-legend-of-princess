import json
import os
import shutil

confirmedFiles = []
with open("./confirmedFiles.json", "r", encoding="utf8") as file:
    confirmedFiles = json.loads(file.read())
confirmedFiles = [name.replace(".wav", ".bwav") for name in confirmedFiles]
confirmedFilesSet = set(confirmedFiles)


voiceprint = []
with open("./snd_speaker.json", "r", encoding="utf8") as file:
    voiceprint = json.loads(file.read())
voiceprintSet = set(voiceprint.keys())


diff = voiceprintSet - confirmedFilesSet

msgs = []
with open("./sndMap.json", "r", encoding="utf8") as file:
    msgs = json.loads(file.read())

sndMapVoiceprint = {}
cache = "cache"
for bwav in diff:
    speaker = voiceprint[bwav]
    speakerFolder = os.path.join(cache,'output', speaker)
    if not os.path.exists(speakerFolder):
        os.mkdir(speakerFolder)
    if not speaker in sndMapVoiceprint.keys():
        sndMapVoiceprint[speaker] = {}
    wav = bwav.replace(".bwav", ".wav")
    try:
        sndMapVoiceprint[speaker][wav] = msgs[bwav]
    except KeyError as e:
        print(bwav)
        continue
    shutil.copyfile(
        os.path.join(cache, wav),
        os.path.join(speakerFolder, wav),
    )

with open("./sndMap_voiceprint.json", "w+", encoding="utf8") as file:
    file.write(json.dumps(sndMapVoiceprint, ensure_ascii=False))
