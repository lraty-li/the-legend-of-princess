import subprocess
import paddle, os
from paddlespeech.cli.vector import VectorExecutor

ffprobe = "ffprobe"
ffmpeg = "ffmpeg"
cacheRoot = "cache"


def subprocessCall(command):
    ffprobeCall = subprocess.Popen(
        command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    out, err = ffprobeCall.communicate()
    if err:
        print("error", err)
        return None
    return out


def genSampleRate(filePath):
    # ffprobe -v error -select_streams a -of default=noprint_wrappers=1:nokey=1 -show_entries stream=sample_rate
    command = [
        ffmpeg,
        "-y",
        "-v",
        "error",
        "-select_streams",
        "a",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        "-show_entries",
        "stream=sample_rate",
        filePath,
    ]
    result = subprocessCall(command)
    return int(result)


def reSample(filepath, newSampleRate="16000",audioSubfix = '.wav'):
    # ffmpeg -i in.m4a -ac 1 -ar 22050 -c:a libmp3lame -q:a 9 out.mp3
    newFileAPath = os.path.join(cacheRoot, filepath.split('\\')[-1].replace('{}'.format(audioSubfix),'-{}{}'.format(newSampleRate, audioSubfix)))
    command = [ffmpeg, "-i", filepath, "-ar", newSampleRate, "-y", newFileAPath]
    result = subprocessCall(command)
    return newFileAPath


def audio2Vector(filepath,vector_executor = VectorExecutor()):
    # vector_executor = VectorExecutor()
    audio_emb = vector_executor(
        model="ecapatdnn_voxceleb12",
        sample_rate=16000,
        config=None,  # Set `config` and `ckpt_path` to None to use pretrained model.
        ckpt_path=None,
        audio_file=filepath,
        device=paddle.get_device(),
        force_yes=True
    )
    return audio_emb


# # score range [0, 1]
# score = vector_executor.get_embeddings_score(audio_emb, test_emb)
# print(f"Eembeddings Score: {score}")

if __name__ == "__main__":
    path = reSample("Dm_BZ_0006_Text_000_b.wav")
    rate = audio2Vector(path)
    print(rate)
