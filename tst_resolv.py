#! /usr/bin/python3
# (c) Copyright 2019-2020, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" code to test out the DNS resolver code """

import json
import sys
import argparse

import resolv
import validation


def run():
    """ main """
    parser = argparse.ArgumentParser(
        description='This is a wrapper to test the resolver code')
    parser.add_argument("-s",
                        "--servers",
                        default="8.8.8.8,1.1.1.1",
                        help="Resolvers to query")
    parser.add_argument("-n",
                        "--name",
                        default="jrcs.net",
                        help="Name to query for")
    parser.add_argument("-t",
                        "--rdtype",
                        default="txt",
                        help="RR Type to query for")
    args = parser.parse_args()

    if not validation.is_valid_host(args.name):
        print(f"ERROR: '{args.name}' is an invalid host name")
        sys.exit(1)

    qry = resolv.Query(args.name, args.rdtype)
    qry.servers = args.servers.split(",")
    print(json.dumps(qry.resolv(), indent=2))


if __name__ == "__main__":
    run()
