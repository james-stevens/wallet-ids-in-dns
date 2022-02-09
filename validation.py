#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" library to run validations """

import re
import socket

is_valid_host_re = re.compile(r'^[0-9a-zA-Z.]{2,255}$')


def is_valid_host(host):
    """ check {host} is a valid DNS hostname """
    return is_valid_host_re.match(host) is not None


def is_valid_ipv4(address):
    """ check {address} is a valid IPv4 address """
    if address is None:
        return False

    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True
