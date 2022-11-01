from converter import Converter
import subprocess
import sys
import os
import time 
from queue import deque

"""
Basic usage of Python Video Converter:

probe: Converter().probe('PATH')

convert: Converter().convert(INPUT_FILE, OUTPUT_FILE, OPTIONS)
--> this returns timecode iterable...
"""


video_queue = deque

args = sys.argv[1:]


default_format = {
    'format': 'mp4',
    'audio': { 'codec': 'aac' },
    'video': { 'codec': 'h264' }
}

CONVERTER = Converter()
    
def main():
    spec = CONVERTER.probe(args[0])
    print(spec.video.codec)

        

        

    
    
if __name__ == '__main__':
    main()
        
    




    