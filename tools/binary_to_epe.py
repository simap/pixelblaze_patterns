#!/usr/bin/env python3
# convert pixelblaze binary file to epe
# V1.0 NW 17th June 2021

import sys, re, struct, json, base64
from lzstring import LZString

# structure of pixelblaze binary file (FW V 3.16)
# first 36 bytes contains offsets and length of sections of file in unsigned integer (litle-endian) format
# eg (2, 36, 13, 49, 968, 1017, 2384, 3401, 2094)
# Not sure about 2 - version number?
# name is at offset 36, length 13
# jpeg image starts at 49, length 968
# bytecode starts at 1017, length 2384
# source plain text starts at 3401 length 2094 (LZString compressed)

header_size = 36

def make_file_name(fname, ext=None):
    fname = re.sub('[^a-zA-Z0-9\n\.]', '_', fname)
    if ext:
        return '{}.{}'.format(fname, ext)
    return fname

def write_epe(epe):
    epe_name = epe.get('name')
    if epe_name:
        epe_fname = make_file_name(epe_name, 'epe')
        with open(epe_fname, 'w') as f:
            f.write(json.dumps(epe, indent=2))
            print('wrote {}'.format(epe_fname))

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: {} [filename] <x> (optional to extract components)".format(sys.argv[0]))
        sys.exit(0)
        
    if len(sys.argv) > 2 and sys.argv[2] == 'x':
        extract = True
        print('Extracting components')
    else:
        extract = False

    filename = sys.argv[1]

    with open(filename, 'rb') as fp:
        data = fp.read()
        
    offsets = struct.unpack('<9I', data[:header_size])
    name_offset = offsets[1]
    name_length = offsets[2]
    jpeg_offset = offsets[3]
    jpeg_length = offsets[4]
    bytecode_offset = offsets[5]
    bytecode_length = offsets[6]
    source_offset = offsets[7]
    source_length = offsets[8]
    #print('offsets: {}'.format(offsets))
    
    id = filename.replace('.bin','')
    name = data[name_offset:name_offset+name_length].decode('UTF-8')
    jpg = data[jpeg_offset:jpeg_offset+jpeg_length]
    bytecode = data[bytecode_offset:bytecode_offset+bytecode_length]
    sourcecode = data[source_offset:source_offset+source_length]
    decoded_source = LZString.decompressFromUint8Array(sourcecode)
    
    epe = {'name': name, 'id': id}
    epe['sources'] = json.loads(decoded_source)
    epe['preview'] = base64.b64encode(jpg).decode('UTF-8')
    
    write_epe(epe)
    
    if extract:
        jpg_fname = make_file_name(name, 'jpeg')
        with open(jpg_fname, 'wb') as fp:
            fp.write(jpg)
            print('extracted {}'.format(jpg_fname))
        
        source_fname = make_file_name(name, 'js')
        with open(source_fname, 'w') as fp:
            if len(epe['sources']) == 1:
                fp.write(epe['sources']['main'])
            elif len(epe['sources']) > 1:
                fp.write('{\n')
                for s_name, source in epe['sources'].items():
                    fp.write('"{}": "{}",\n'.format(s_name, source))
                fp.write('\n}')
            else:
                print('no source code found')
            print('extracted {}'.format(source_fname))
            
        bytecode_fname = make_file_name(name, 'bc')
        with open(bytecode_fname, 'wb') as fp:
            fp.write(bytecode)
            print('extracted {}'.format(bytecode_fname))
