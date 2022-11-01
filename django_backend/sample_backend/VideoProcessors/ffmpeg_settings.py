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

default_format = {
    'format': 'mp4',
    'audio': { 'codec': 'aac' },
    'video': { 'codec': 'h264' }
}

CONVERTER = Converter()
        
    




    