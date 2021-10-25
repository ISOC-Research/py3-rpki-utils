#!/usr/bin/env python3

from os.path import dirname, abspath, join
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

roa = ROA.derReadFile(sys.argv[1])
roa.parse()
print(roa.getASID(), " ".join(roa.v4_prefixes + roa.v6_prefixes))
