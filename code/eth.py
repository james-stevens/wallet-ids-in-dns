#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" translate a <wallet name> into a <wallet id> """

import requests
import json

import servers
import resolv


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Content-type': 'application/dns-json',
    'Accept': 'application/json'
    }


def get_eth_txt(hostname):
    url = f"https://{servers.ETH_GATEWAY}?type=TXT&name={hostname}"
    try:
        r = requests.request("get",url, headers=HEADERS)
        resjs = json.loads(r.content)
        resjs["Flags"] = [flag for flag in resolv.DNS_FLAGS if flag in resjs and resjs[flag]]
        return resjs
    except Exception as err:
        return None

    return None



if __name__ == "__main__":
    # this is for testing only
    js = get_eth_txt("wealdtech.eth")
    print(json.dumps(js,indent=2))
