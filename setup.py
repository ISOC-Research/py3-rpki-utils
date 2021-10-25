from setuptools import setup, Extension

packages = ["rpki", "rpki.POW" ]

setup (name = 'rpki',
    version = '0.1',
    description = 'Utility functions for RPKI',
    license = 'BSD',
    ext_modules = [Extension("rpki.POW._POW", ["ext/POW.c"],
        include_dirs = ["/usr/local/include", "h"],
        extra_link_args = ["-lcrypto" ])]
)
