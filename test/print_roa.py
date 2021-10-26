#!/usr/bin/env python3

# Copyright (C) 2021  The Internet Society ("ISOC")
# Copyright (C) 2015-2016  Parsons Government Services ("PARSONS")
# Portions copyright (C) 2014  Dragon Research Labs ("DRL")
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notices and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND PARSONS, DRL and ISOC DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL
# PARSONS OR DRL BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Pretty-print the content of a ROA.  Does NOT attempt to verify the
signature.
"""

from os.path import dirname, abspath, join
import argparse
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

import rpki.POW

class ROA(rpki.POW.ROA):

    v4_prefixes = None
    v6_prefixes = None

    @staticmethod
    def _format_prefix(p):
        if p[2] in (None, p[1]):
            return "%s/%d" % (p[0], p[1])
        else:
            return "%s/%d-%d" % (p[0], p[1], p[2])

    def parse(self):
        self.extractWithoutVerifying()
        v4, v6 = self.getPrefixes()
        self.v4_prefixes = [self._format_prefix(p) for p in (v4 or ())]
        self.v6_prefixes = [self._format_prefix(p) for p in (v6 or ())]


parser = argparse.ArgumentParser(description = __doc__)
parser.add_argument("--brief", action = "store_true", help = "show only ASN and prefix(es)")
parser.add_argument("--cms", action = "store_true", help = "print text representation of entire CMS blob")
parser.add_argument("--signing-time", action = "store_true", help = "show SigningTime in brief mode")
parser.add_argument("roas", nargs = "+", type = ROA.derReadFile, help = "ROA(s) to print")
args = parser.parse_args()

for roa in args.roas:
    roa.parse()
    if args.brief:
        if args.signing_time:
            print(roa.signingTime())
        print(roa.getASID(), " ".join(roa.v4_prefixes + roa.v6_prefixes))
    else:
        print("ROA Version:   ", roa.getVersion())
        print("SigningTime:   ", roa.signingTime())
        print("asID:          ", roa.getASID())
        if roa.v4_prefixes:
            print(" addressFamily:", 1)
            for prefix in roa.v4_prefixes:
                print("     IPAddress:", prefix)
        if roa.v6_prefixes:
            print(" addressFamily:", 2)
            for prefix in roa.v6_prefixes:
                print("     IPAddress:", prefix)
        if args.cms:
            print(roa.pprint())
            for cer in roa.certs():
                print(cer.pprint())
            for crl in roa.crls():
                print(crl.pprint())
        print
