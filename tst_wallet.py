#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" translate a <wallet name> into a <wallet id> """

import json
import argparse

import wallet


def run():
    """ main """
    parser = argparse.ArgumentParser(
        description='This is a wrapper to test the wallet code')
    parser.add_argument("-w",
                        "--wallet",
                        default="$btc@jrcs.net",
                        help="Wallet to find")
    parser.add_argument("-s",
                        "--servers",
                        default="8.8.8.8,1.1.1.1",
                        help="Resolvers to query")

    args = parser.parse_args()

    my_wallet = wallet.Wallet(args.wallet, servers=args.servers)
    my_wallet.resolv()
    if my_wallet.wallet_id is not None:
        print(json.dumps(my_wallet.wallet_id, indent=2))
    else:
        print(f"ERROR: Wallet name '{args.wallet}' failed to lookup")


if __name__ == "__main__":
    run()
