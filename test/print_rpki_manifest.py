#!/usr/bin/env python3

from os.path import dirname, abspath, join
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

mft = rpki.POW.Manifest.derReadFile(sys.argv[1])
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
    print(mft.pprint())
    for cer in mft.certs():
       print(cer.pprint())
    for crl in mft.crls():
       print(crl.pprint())
    print
