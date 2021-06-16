#!/usr/bin/env python3
# Use this to create epe files from source files in patterns/
# assumes structure as in https://github.com/simap/pixelblaze_patterns/tree/main/patterns/example
# or source files only to be in src/
# search for source will be from the current directory, or pass the path as the first argument.

import sys, os, json, re, base64

search_dir = './'
if len(sys.argv) > 1:
    search_dir = sys.argv[1]

script_dir = os.path.dirname(search_dir)
indirs = [os.path.join(script_dir, dir) for dir in ["patterns", "src"]]
outdir = os.path.join(script_dir, "epe")

def write_epe(epe):
    epe_name = epe.get('name')
    if epe_name:
        epe_fname = '{}.epe'.format(re.sub('[^a-zA-Z0-9\n\.]', '_', epe_name))
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open(os.path.join(outdir, epe_fname), 'w') as f:
            f.write(json.dumps(epe, indent=2))
            print('wrote {}'.format(epe_fname))
            
def make_epe(infile, epe, name=None):
    if name:
        epe.update({'name': name})
        name = 'main'
    with open(infile, 'rb') as src:
        if infile.endswith('.js'):
            epe.setdefault('sources', {})
            if not name:
                name = os.path.basename(infile).replace('.js','')
            epe['sources'][name] = src.read().decode('UTF-8')
        elif infile.endswith('.json'):
            epe.update(json.load(src))
        elif infile.endswith('.jpg'):
            epe['preview'] = base64.b64encode(src.read()).decode('UTF-8')
    return epe

for indir in indirs:
    if os.path.isdir(indir):
        for f_or_dir in os.listdir(indir):
            epe = {}
            in_path = os.path.join(indir, f_or_dir)
            if os.path.isdir(in_path):
                print('searching: {}'.format(f_or_dir))
                for root, dirs, files in os.walk(in_path, topdown=False):
                    for name in files:
                        infile = os.path.join(root, name)
                        epe = make_epe(infile, epe)       
            else:   #its a file
                print('checking file: {}'.format(f_or_dir))
                epe = make_epe(in_path, epe, name=f_or_dir.replace('.js',''))
            write_epe(epe)