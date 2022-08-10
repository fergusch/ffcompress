import os
from shutil import which
from subprocess import Popen, PIPE

NO_COLOR = False
NO_ANIMATION = False

def c(text, color, bold=False):
    color_escapes = {
        'k': 30, # black
        'r': 31, # red
        'g': 32, # green
        'y': 33, # yellow
        'b': 34, # blue
        'm': 35, # magenta
        'c': 36, # cyan
        'e': 37  # grey
    }
    if not NO_COLOR:
        return f'\033[{int(bold)};{color_escapes[color]}m{text}\033[0m'
    return text

def cb(text, color):
    return c(text, color, bold=True)

def get_len_seconds(file):
    if not which('ffprobe'):
        raise ModuleNotFoundError('ffprobe is not installed')
    p = Popen([which('ffprobe'),
               '-v', 'error',
               '-show_entries',
               'format=duration',
               '-of', 'default=noprint_wrappers=1:nokey=1',
               file], stdout=PIPE)
    return float(p.communicate()[0].decode('utf-8'))

def get_required_bitrate(file, bytes):
    return ((bytes*8) / get_len_seconds(file))*0.97

def blocks_to_bytes(blocks, block_size):
    if block_size == 'GB':
        return blocks * (10**9)
    elif block_size == 'MB':
        return blocks * (10**6)
    elif block_size == 'KB':
        return blocks * (10**3)
    else:
        return blocks

def bytes_to_blocks(bytes, block_size):
    if block_size == 'GB':
        return bytes // (10**9)
    elif block_size == 'MB':
        return bytes // (10**6)
    elif block_size == 'KB':
        return bytes //  (10**3)
    else:
        return bytes

def get_compress_pipe(input_file, output_file, blocks, block_size):
    if not which('ffmpeg'):
        raise ModuleNotFoundError('ffmpeg is not installed')
    return Popen([which('ffmpeg'),
                  '-i', os.path.abspath(input_file),
                  '-b:v', str(get_required_bitrate(input_file, blocks_to_bytes(blocks, block_size))),
                  '-v', 'quiet',
                  '-stats',
                  '-progress', 'pipe:1',
                  '-y',
                  os.path.abspath(output_file)], stdout=PIPE, stderr=PIPE)
