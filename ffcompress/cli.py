import argparse
import re
import os
import sys

from ._version import __version__
from . import ffcompress
from .utils import c, cb, blocks_to_bytes, bytes_to_blocks

def main():
    parser = argparse.ArgumentParser(description='ffmpeg-based video compression tool')
    parser.add_argument('-v', '--version', action='version', 
                        version=f'ffcompress {__version__}')
    parser.add_argument('FILE', help='File to compress')
    parser.add_argument('SIZE', help="Size to compress to e.g. '1gb', '50mb', '200kb'")
    parser.add_argument('-y', '--yes',
                        dest='confirm_overwrite',
                        action='store_true',
                        help='Overwrite output files without asking')
    args = parser.parse_args()

    try:

        if not re.match(r'^(\d+)((g|m|k)b?|b)$', args.SIZE.lower()):
            parser.print_help(sys.stderr)
            print()
            raise TypeError(f"Size argument {cb(args.SIZE, 'r')} not understood, see usage")

        if not os.path.exists(args.FILE):
            raise FileNotFoundError(f"File {cb(args.FILE, 'r')} not found")
        
        blocks = int(re.findall(r'^(\d+)', args.SIZE)[0])
        block_size = 'GB' if 'g' in args.SIZE.lower() else \
                     'MB' if 'm' in args.SIZE.lower() else \
                     'KB' if 'k' in args.SIZE.lower() else 'B'
        
        if os.path.getsize(args.FILE) <= blocks_to_bytes(blocks, block_size):
            raise ValueError(f"File {cb(args.FILE, 'r')} is already smaller than {blocks} {block_size}")

        output_file = f"{args.FILE.rsplit('.', 1)[0]}_Compressed.mp4"
        if os.path.exists(output_file) and not args.confirm_overwrite:
            overwrite = input(f"{c('▲', 'y')} File {c(output_file, 'y')} already exists. Overwrite? (y/N): ")
            if overwrite != 'y':
                raise KeyboardInterrupt
        
        ffcompress.pbar(args.FILE, output_file, blocks, block_size)

        output_size = 1/blocks_to_bytes(1/os.path.getsize(output_file), block_size)

        print(c('✓', 'g'), 'Compressed', c(args.FILE, 'g'), 'to', c(f'{output_size:.1f} {block_size}', 'c'))
        print(c('➔', 'e'), 'Output file:', c(output_file, 'e'))

    except KeyboardInterrupt:
        print(c('× Operation cancelled', 'r'))
    except Exception as e:
        # print(c(f'{type(e).__name__}:', 'r'))
        print(c('×', 'r'), str(e))
        sys.exit(1)
