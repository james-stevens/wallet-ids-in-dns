#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" default DNS Servers for different TLD areas """

import os

ICANN_SERVERS = "8.8.8.8,1.1.1.1"
HANDSHAKE_SERVERS = "109.169.23.69"
ETH_GATEWAY = "eth.link/dns-query"

if "ICO_ICANN_SERVERS" in os.environ:
    icann_servers = os.environ["ICO_ICANN_SERVERS"].split(",")
else:
    icann_servers = ICANN_SERVERS.split(",")

if "ICO_HANDSHAKE_SERVERS" in os.environ:
    handshake_servers = os.environ["ICO_HANDSHAKE_SERVERS"].split(",")
else:
    handshake_servers = HANDSHAKE_SERVERS.split(",")

if "ICO_ETH_GATEWAY" in os.environ:
    eth_gateway = os.environ["ICO_ETH_GATEWAY"].strip()
else:
    eth_gateway = ETH_GATEWAY.strip()
