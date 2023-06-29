# -*- coding: UTF-8 -*-
import json
from PIL import Image
import os
import audio_to_vector
from annoy import AnnoyIndex
from paddlespeech.cli.vector import VectorExecutor

# https://github.com/currentslab/awesome-vector-search


def getSpeakerId(speaker, speakerMap):
    speakerKeys = speakerMap.keys()
    if speaker in speakerKeys:
        speakerId = speakerMap[speaker]
    else:
        speakerId = len(speakerKeys)
        speakerMap[speaker] = speakerId
    return speakerId


if __name__ == "__main__":
    VECTOR_DIM = 192
    N_TREE = 50

    ann = AnnoyIndex(VECTOR_DIM, "angular")
    speakerMap = {}
    vectorExecutor = VectorExecutor()

    speakerRoot = r"D:\game\dump_totk_files\000-workplace\collect_voice\output"
    speakerFolders = os.listdir(speakerRoot)

    counter = 0
    for folder in speakerFolders:
        wavs = os.listdir(os.path.join(speakerRoot, folder))
        for wav in wavs:
            # Elasticsearch？
            wavPath = os.path.join(speakerRoot, folder, wav)
            newAudioPath = audio_to_vector.reSample(wavPath)
            audioVtct = audio_to_vector.audio2Vector(
                newAudioPath,
                vectorExecutor
            )
            speakerMap[counter] = folder
            ann.add_item(counter, audioVtct)
            counter += 1
    # build annoy index
    ann.build(N_TREE)
    ann.save("./speakers.ann")
    with open("./speakerMap.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(speakerMap))
    # images = os.listdir(font_all_image)
    # charToVetctor = {}
    # for img in images:
    #   imgName = img[0:-4] #".png"

    #   # Elasticsearch？
    #   image = Image.open(os.path.join(font_all_image, img))
    #   vetcor = img2Vetor(image)
    #   ann.add_item(int(imgName), vetcor)

    # # build annoy index
    # ann.build(40)
    # ann.save('ttf_annoy.ann')
    # np.save("ttf_charToVetor.npy",charToVetctor ,allow_pickle=True)
