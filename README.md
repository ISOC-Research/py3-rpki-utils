# Python 3 utilities for RPKI

This is a Python 3 port of the utility functions from Dragon Research Labs
[RPKI Toolkit](https://github.com/dragonresearch/rpki.net), also known as
"rpki.net".  This is intended as a proof of concept / feasibility study more
than anything else.

Installation and Usage instructions.

```shell
$ git clone https://github.com/aftabsiddiqui/py3-rpki-utils.git
$ cd py3-rpki-utils
$ python3 setup.py build
$ cp build/*/*/*/_POW*.so rpki/POW/_POW.so
$ cd print
```

```shell
$ python3 print_roa.py --help

```
usage: print_roa.py [-h] [--brief] [--cms] [--signing-time] roas [roas ...]

Pretty-print the content of a ROA. Does NOT attempt to verify the signature.

positional arguments:
roas ROA(s) to print

optional arguments:
-h, --help show this help message and exit
--brief show only ASN and prefix(es)
--cms print text representation of entire CMS blob
--signing-time show SigningTime in brief mode


```shell
$ python3 print_rpki_manifest.py -h

```
usage: print_rpki_manifest.py [-h] [--cms] manifests [manifests ...]

positional arguments:
manifests manifest(s) to print

optional arguments:
-h, --help show this help message and exit
--cms print text representation of entire CMS blob
