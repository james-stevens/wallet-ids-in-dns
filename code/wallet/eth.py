#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" translate a <wallet name> into a <wallet id> """

from syslog import syslog
import json
import requests

import servers

HEADERS = {
    'Content-type': 'application/dns-json',
    'Accept': 'application/json'
}


def get_eth_txt(hostname):
    """ load TXT DNS data for {hostname} & return in DoH format """
    url = f"https://{servers.eth_gateway}?type=TXT&name={hostname}"
    try:
        resp = requests.request("get", url, headers=HEADERS)
        return json.loads(resp.content)
    except Exception as err:  # pylint: disable=broad-except
        raise ValueError(f"Requst to {servers.eth_gateway} failed")

    raise ValueError("Unexpected error in ETH processing")


if __name__ == "__main__":
    # this is for testing only
    js = get_eth_txt("wealdtech.eth")
    print(json.dumps(js, indent=2))
