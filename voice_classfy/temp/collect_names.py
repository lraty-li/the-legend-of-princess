# -*- coding: UTF-8 -*-
import json
import os


if __name__ == "__main__":
    VECTOR_DIM = 192
    N_TREE = 50

    confirmedFiles = []

    speakerRoot = r"D:\game\dump_totk_files\000-workplace\collect_voice\output"
    speakerFolders = os.listdir(speakerRoot)
    for folder in speakerFolders:
        wavs = os.listdir(os.path.join(speakerRoot, folder))
        confirmedFiles += wavs
   
    # build annoy index
    with open("./confirmedFiles.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(confirmedFiles))
