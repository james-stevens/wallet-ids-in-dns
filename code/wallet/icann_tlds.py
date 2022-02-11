#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" Load ICANN TLDs from text file """

import os

FILE = "icann_tlds.txt"


def do_tld_load(path):
    """ read {path} list of tlds & set True in dict """
    with open(path, "r") as fd_id:
        return {r.strip(): True for r in fd_id.readlines()}


def load_tlds_from_file():
    """ load icann tlds list from appropriate file """
    if "ICO_ICANN_TLDS" in os.environ:
        return do_tld_load(os.environ["ICO_ICANN_TLDS"])

    if os.path.isfile(FILE):
        return do_tld_load(FILE)

    path = "/usr/local/etc/" + FILE
    if os.path.isfile(path):
        return do_tld_load(path)

    return None


tlds = load_tlds_from_file()
if tlds is None:
    tlds = {}
else:
    if "ICO_ICANN_EXCLUDE" in os.environ:
        for rm_tld in os.environ["ICO_ICANN_EXCLUDE"].split(","):
            if rm_tld in tlds:
                del tlds[rm_tld]
