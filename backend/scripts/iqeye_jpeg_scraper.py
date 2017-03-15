#!/usr/bin/env python3

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "MIT" # as per https://github.com/simsong/privacy-auditing-book/book/ch-jpeg/jpeg_scan.py
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import struct
import argparse
import os
import mmap

def validate_jpeg(fn):
  f = open(fn,"rb")
  
  # compute line count
  for lineno, content in enumerate(f):
    pass
  
  # reset file pointer back to zero after enumerate()
  f.seek(0)
  
  data = f.read() # TODO(use iterator, generator?)
  pos = 0
  comment = 0
  
  while pos+2 <= len(data):
    if data[pos] != 0xFF:
      #print("{} No Marker FF @ loc {}  ({} found)".format(fn,pos,data[pos]))
      return
    marker = data[pos+1]
    
    # Decode the fixed-size markers
    if marker==0xD8:  # SOI
      pos += 2;
      continue

    if (marker >= 0xD0 and marker <= 0xD8): # RSTn
      pos += 2;
      continue
    
    if marker==0xD9: # EOI
      extra = len(data)-(pos+2)
      #if extra: print("  EXTRA BYTES: {}".format(extra))
      return       # validated!

    # Decode the SOS segment
    if marker==0xDA: # Found SOS; scan for the EOI
      eoi_loc = data.find(b'\xFF\xD9',pos)
      if eoi_loc>0:
        pos = eoi_loc;
        continue 
      print("  NO EOI")
      return

    # Get the length, add it, then loop
    try:
      segment_len = struct.unpack('>H',data[pos + 2:pos + 4])[0]
      if marker==0xFE:
        if comment == 1: # grab only the IQeye JSON
          print("{},{}".format(fn, str(data[pos + 4:pos + 2 + segment_len], 'utf-8')))
          # Additional decoding could go here
        comment += 1
      pos += 2 + segment_len
    except struct.error:
      break               # end of file?

if __name__=="__main__":

  parser = argparse.ArgumentParser(description="Search and process JPEGs in local file system")
  parser.add_argument("path",nargs="+",help="Path to search")
  args = parser.parse_args()

  def is_jpeg_fn(fn):
    return os.path.splitext(fn)[1].lower() in ['.jpg','.jpeg']
  
  for fn in args.path:
    if os.path.isdir(fn):
      for (dirpath, dirnames, filenames) in os.walk(fn):
        for name in filter(is_jpeg_fn,filenames):
            byte_size = os.path.getsize(os.path.join(dirpath,name))
            validate_jpeg(os.path.join(dirpath,name))
      else: #TODO(bug here where the actop-level dir is called as JPEG file)
        validate_jpeg(fn)

# sample IQeye JPEG header
# 00 50 1a 22 0e 83 is the MAC
# 3b is the camera model
# then the JSON 
'''
00000000  ff d8 ff e0 00 10 4a 46  49 46 00 01 02 01 00 60  |......JFIF.....`|
00000010  00 60 00 00 ff fe 00 09  00 50 1a 22 0e 83 3b ff  |.`.......P."..;.|
00000020  fe 00 a2 7b 22 49 51 69  6d 61 67 65 22 3a 7b 22  |...{"IQimage":{"|
00000030  73 65 71 75 65 6e 63 65  22 3a 38 35 30 33 38 36  |sequence":850386|
00000040  32 2c 22 74 69 6d 65 22  3a 31 34 34 39 36 32 33  |2,"time":1449623|
00000050  35 35 38 31 33 30 2c 22  65 76 65 6e 74 22 3a 5b  |558130,"event":[|
00000060  22 6d 6f 74 69 6f 6e 22  5d 2c 22 6d 6f 74 69 6f  |"motion"],"motio|
00000070  6e 57 69 6e 64 6f 77 73  22 3a 5b 31 5d 2c 22 69  |nWindows":[1],"i|
00000080  6d 67 6a 64 62 67 22 3a  22 20 30 30 30 2f 30 32  |mgjdbg":" 000/02|
00000090  30 3a 31 33 2f 33 30 2f  31 33 32 3a 30 37 30 2f  |0:13/30/132:070/|
000000a0  30 39 33 2f 32 39 2f 30  2f 34 35 2f 37 30 2f 32  |093/29/0/45/70/2|
000000b0  30 2f 30 30 3a 30 37 2f  30 36 2f 30 37 3a 39 62  |0/00:07/06/07:9b|
000000c0  22 7d 7d ff db 00 43 00  0b 08 08 0a 08 07 0b 0a  |"}}...C.........|
000000d0  09 0a 0d 0c 0b 0d 11 1c  12 11 0f 0f 11 22 19 1a  |............."..|
000000e0  14 1c 29 24 2b 2a 28 24  27 27 2d 33 41 37 2d 30  |..)$+*($''-3A7-0|
'''
