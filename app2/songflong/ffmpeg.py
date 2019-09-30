from imageio.plugins.ffmpeg import get_exe
from subprocess import DEVNULL
import os
import subprocess as sp
import proglog


def subprocess_call(cmd):
    """
    Executes the given subprocess command.

    :param cmd: The command
    :type cmd: str
    """
    logger = proglog.default_bar_logger('bar')
    logger(message='FFMPEG - Running:\n>>> "+ " ".join(cmd)')

    popen_params = {"stdout": DEVNULL,
                    "stderr": sp.PIPE,
                    "stdin": DEVNULL}

    if os.name == "nt":  # Support for the inferior OS
        popen_params["creationflags"] = 0x08000000

    proc = sp.Popen(cmd, **popen_params)

    out, err = proc.communicate()  # proc.wait()
    proc.stderr.close()

    if proc.returncode:
        logger(message='FFMPEG - Command returned an error')
        raise IOError(err.decode('utf8'))
    else:
        logger(message='FFMPEG - Command successful')

    del proc


def ffmpeg_merge_video_audio(video, audio, output):
    """
    Merges video and audio files into a single movie file.

    :param video: The Path to the video file
    :type video: Path
    :param audio: The Path to the audio file
    :type audio: Path
    :param output: The destination Path for the merged movie file
    :param output: Path
    """
    cmd = [get_exe(), "-y", "-i", str(audio), "-i", str(video),
           "-vcodec", 'copy', "-acodec", 'copy', str(output)]

    subprocess_call(cmd)
