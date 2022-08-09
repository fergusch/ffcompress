import re
import os
import itertools
import time

from shutil import get_terminal_size
from sys import stdout
from .utils import c, cb, get_len_seconds, get_compress_pipe, blocks_to_bytes

def pbar(input_file, output_file, blocks, block_size):
    pipe = get_compress_pipe(input_file, output_file, blocks, block_size)
    len_seconds = get_len_seconds(input_file)
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    progress = 0
    curr_size = 1/blocks_to_bytes(1/os.path.getsize(input_file), block_size)
    text = f"Compressing {c(os.path.basename(input_file), 'y')} {cb(f'({curr_size:.1f} {block_size})', 'k')} to ≤ {blocks} {block_size}"
    try:
        while pipe.poll() is None:
            pw = get_terminal_size()[0] - len(text)
            stdout.write('\r')
            stdout.write(cb(next(spinner), 'k'))
            stdout.write(' ' + text)
            out_time = re.findall('^out_time_ms=(\d+)$', pipe.stdout.readline().decode('utf-8'))
            if out_time:
                progress = int((((float(out_time[0]) / 10**6) * 2) / (len_seconds+1))*pw)
            stdout.write(cb(' [', 'k'))
            stdout.write(c('━'*progress, 'e'))
            stdout.write(c('━'*(pw-progress), 'k'))
            stdout.write(f' {int((progress/pw)*100)}%')
            stdout.write(cb(']', 'k'))
            stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pipe.kill()
        raise
    finally:
        stdout.write('\r' + ' '*get_terminal_size()[0] + '\r')
        stdout.flush()
