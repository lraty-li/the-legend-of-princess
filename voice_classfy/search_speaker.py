import os
import shutil
import json
import audio_to_vector
from annoy import AnnoyIndex
from paddlespeech.cli.vector import VectorExecutor
import math

streamsRoot = (
    r"E:\totk_dump\totk_dump\secure\totk_dump\1\Voice\Resource\JPja\EventFlowMsg"
)
workPlaceRoot = "cache"
vgmstream = r"D:\game\dump_totk_files\vgmstream-win64\vgmstream-cli.exe"

files = os.listdir(streamsRoot)
folders = [fold for fold in files if os.path.isdir(os.path.join(streamsRoot, fold))]

sndMap = []
with open("./sndMap.json", "r", encoding="utf8") as file:
    sndMap = json.loads(file.read())
sndMapKeys = set(sndMap.keys())

partSpeakerMap = []
with open("./speakerMap.json", "r", encoding="utf8") as file:
    partSpeakerMap = json.loads(file.read())


vectorExecutor = VectorExecutor()


VECTOR_DIM = 192
SEARCH_K = -1
ann = AnnoyIndex(VECTOR_DIM, "angular")
ann.load('./speakers.ann', prefault= True) # super fast, will just mmap the file
sum = ann.get_n_items()
for i in range(sum):
    ann.get_item_vector(i)

def bwav2wav(filePathNoExtension):
    os.system(
        "{} {}.bwav -o {}.wav".format(
            vgmstream, filePathNoExtension, filePathNoExtension
        )
    )

completeSpeakerMap = {}

for fold in folders:
    namePrefix = fold.split("_Stream")[0]
    subStreams = os.listdir(os.path.join(streamsRoot, fold))
    for subStream in subStreams:
        if(subStream == 'Dm_BZ_0007_Text_002_b.bwav'):
            print()
        # shutil.copyfile(
        #     os.path.join(streamsRoot, fold, subStream),
        #     os.path.join(workPlaceRoot, subStream),
        # )
        # # search speaker
        # noExtAudioPath = os.path.join(workPlaceRoot, subStream).replace(".bwav", "")
        # bwav2wav(noExtAudioPath)
        # newAudioPath = audio_to_vector.reSample(noExtAudioPath + ".wav")
        newAudioPath = os.path.join(workPlaceRoot, subStream.replace('.bwav'.format(),'-{}{}'.format(16000, '.wav')))
        audioVtct = audio_to_vector.audio2Vector(newAudioPath, vectorExecutor)
        result = ann.get_nns_by_vector(audioVtct, 1 , search_k = SEARCH_K ,include_distances=True)
        #THREAD_HOLD = 0.447   sqrt(2-2*0.80)
        if(result[1][0] < 0.753):
            completeSpeakerMap[subStream] = partSpeakerMap[str(result[0][0])]
        # https://github.com/spotify/annoy/issues/112
    #   try:
    #     sndMap[subStream] = snds[subStream.replace('.bwav', '')]
    #   except KeyError as e:
    #     print('not found:')
    #     print(subStream, snds)
with open("./snd_speaker.json", "w+", encoding="utf8") as file:
    file.write(json.dumps(completeSpeakerMap, ensure_ascii=False))

print("DONE")
