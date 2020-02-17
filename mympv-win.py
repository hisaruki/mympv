#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, DEVNULL
import argparse
import re
import sys
from magic import Magic
from mimetypes import guess_type
import tempfile
from pathlib import Path
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("paths", nargs="*")
parser.add_argument("--order", default="default")
parser.add_argument("--reverse", action="store_true")
parser.add_argument("--prefetch", action="store_true")
parser.add_argument("--terminal", action="store_true")
args = parser.parse_args()


#os.chdir(str(Path(__file__).parent))
td = tempfile.TemporaryDirectory()
magic = Magic(mime=True)
paths = []

if len(args.paths) == 0:
    if args.order == "default":
        args.order = "natural"
    inputs = sys.stdin
else:
    inputs = args.paths

def checkmime(p, ln):
    lp = None
    if ln:
        lp = Path(td.name) / Path(ln)
    if args.prefetch:
        lp = Path(td.name) / Path(p.name)
    try:
        str(p).encode("cp932").decode("cp932")
    except:
        lp = Path(td.name) / Path(p.name.encode("cp932", "ignore").decode("cp932"))
    if lp:
        lp.symlink_to(p)

    mime, _ = guess_type(p.name)
    if not mime:
        try:
            mime = magic.from_buffer(p.open("rb").read(1024))
        except:
            mime = None
            p = None
    if mime:
        if re.match(r'(image|video)', mime):
            if lp:
                p = lp
    return p

if len(args.paths) != 1:
    for line in inputs:
        #sys.stderr.write(line + "\n")
        line = line.strip()
        line = line.split("\t")
        l = line[0]
        ln = None
        if len(line) == 2:
            ln = line[1]
        try:
            l = Path(re.sub(r'^file://', '', l))
            if l.exists():
                l = checkmime(l, ln)
                if l:
                    paths.append(l)
        except:
            pass
else:
    line = inputs[0]
    line = line.strip()
    line = line.split("\t")
    l = Path(os.path.abspath(line[0]))
    if l.is_dir():
        cur = l.iterdir()
    else:
        cur = l.parent.iterdir()
    for p in cur:
        ln = None
        p = checkmime(p, ln)
        if p:
            paths.append(p)

try:
    mpv = os.environ['USERPROFILE'] + '/Public/mympv/mpv.com'
except:
    mpv = 'mpv'
proc = [mpv]
stdout = None
if args.terminal:
    proc.append("--terminal")
    stdout = None
if len(paths):
    if args.order != "natural":
        paths = list(set(paths))
    if args.order == "default":
        args.order = "filename"
        ils = list(filter(lambda x: re.search(r'[0-9a-z]{32}$', x.stem), paths))
        if len(ils) / len(paths) >= 0.33:
            args.order = "mtime"

    if args.order == "filename":
        paths = sorted(paths, key=lambda x: x.name, reverse=args.reverse)

    if args.order == "mtime":
        paths = sorted(paths, key=lambda x: x.stat().st_mtime,
                       reverse=args.reverse)
    playlist_start = 0

    if len(args.paths):
        first = Path(args.paths[0])
        try:
            if not first.is_dir():
                playlist_start = [x.name for x in paths].index(first.name)
            proc.append("--playlist-start=" + str(playlist_start))
        except:
            pass

os.chdir(str(Path(__file__).parent))


#proc += [str(x) for x in paths]

playlist = Path(td.name) / Path("playlist.txt")
def c(p):
    if p.drive.find('\\') == 0:
        return str(p)
    else:
        return p.as_uri()
playlist.write_text("\n".join([c(p) for p in paths]), encoding="utf-8")
proc += ["--playlist={}".format(playlist)]

proc = Popen(proc, stdout=stdout)

if args.prefetch:
    for path in paths:
        if path.is_symlink():
            b = path.read_bytes()
            path.unlink()
            path.write_bytes(b)
proc.communicate()
sys.stderr.write("\n")