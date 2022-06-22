#!/usr/bin/env python3

# Copyright (C) 2021  The Internet Society ("ISOC")
# Copyright (C) 2015-2016  Parsons Government Services ("PARSONS")
# Portions copyright (C) 2014  Dragon Research Labs ("DRL")
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notices and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND PARSONS AND DRL DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL
# PARSONS OR DRL BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from os.path import dirname, abspath, join
import argparse
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

"""
Pretty-print the content of a manifest.  Does NOT attempt to verify the
signature.
"""

import rpki.POW
import rpki.oids

argparser = argparse.ArgumentParser(description = __doc__)
argparser.add_argument("--cms", action = "store_true", help = "print text representation of entire CMS blob")
argparser.add_argument("manifests", nargs = "+", type = rpki.POW.Manifest.derReadFile, help = "manifest(s) to print")
args = argparser.parse_args()

for mft in args.manifests:
    mft.extractWithoutVerifying()
    print("Manifest Version:", mft.getVersion())
    print("SigningTime:     ", mft.signingTime())
    print("Number:          ", mft.getManifestNumber())
    print("thisUpdate:      ", mft.getThisUpdate())
    print("nextUpdate:      ", mft.getNextUpdate())
    print("fileHashAlg:     ", rpki.oids.oid2name(mft.getAlgorithm()))
    for i, fah in enumerate(mft.getFiles()):
        name, obj_hash = fah
        print("fileList[%3d]:    %s %s" % (i, ":".join(("%02X" % h for h in obj_hash)), name))
    if args.cms:
        print(mft.pprint())
        for cer in mft.certs():
            print(cer.pprint())
        for crl in mft.crls():
            print(crl.pprint())
    print
