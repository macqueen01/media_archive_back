from converter import Converter
import subprocess
import sys
from queue import deque

"""
Basic usage of Python Video Converter:

probe: Converter().probe('PATH')

convert: Converter().convert(INPUT_FILE, OUTPUT_FILE, OPTIONS)
--> this returns timecode iterable...
"""

default_format = {
    'format': 'mp4',
    'audio': { 'codec': 'aac' },
    'video': { 'codec': 'h264' }
}

video_queue = deque

args = sys.argv[1:]

    
def main():
    conv = Converter()
    timecodes = conv.convert(args[0], args[1], default_format, twopass = False)
    for timecode in timecodes:
        print(f"{args[2]} in progress... {timecode}")
    
    
if __name__ == '__main__':
    main()
        
    




    