from .ffmpeg_settings import default_format, CONVERTER 
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



    
def main():
    timecodes = CONVERTER.convert(args[0], args[1], default_format, twopass = False, timeout = None)
    for timecode in timecodes:
        print(timecode)

        

        

    
    
if __name__ == '__main__':
    main()
        
    