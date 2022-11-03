from converter import Converter
import asyncio
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
    

    
async def main():

    in_path = args[0]
    out_path = args[1]

    result = await check_dir(out_path)

    if (result == 0):
        return 0

    timecodes = CONVERTER.convert(in_path, out_path, default_format, twopass = False, timeout = None)
    for timecode in timecodes:
        print(timecode)
        
    return 1

        
async def check_dir(out_dir):
    out_dirname, i = os.path.split(out_dir)

    if (not os.path.isdir(out_dirname)):
        print('checking...')
        os.makedirs(out_dirname)
    elif (os.path.isdir(out_dir)):
        print("file name needs to be differed")
        return 0
    return 1
        

    
    
if __name__ == '__main__':
    asyncio.run(main())
        
    