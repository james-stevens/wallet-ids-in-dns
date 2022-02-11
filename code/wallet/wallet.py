#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" translate a <wallet name> into a <wallet id> """

import json
import argparse

import resolv
import validation
import eth
import servers
import icann_tlds

TXT_RR_TYPE_ID = 16
reserved = {"tag": True}


def find_coin(fields):
    """ find the coin name used in this TXT """
    for fld in fields:
        if fld not in reserved:
            return fld
    return ""


class Wallet:  # pylint: disable=too-few-public-methods
    """ translate a <wallet> name into a wallet id as a JSON, or None """
    def __init__(self, wallet, local_servers=None):
        self.hostname = None
        self.coin = None
        self.tag = ""
        self.wallet_name = None
        self.wallet_id = None
        if local_servers is not None:
            self.servers = local_servers.split(",")
        else:
            self.servers = None

        if wallet[0:6] == "ico://":
            self.wallet_name = wallet[6:]
        elif wallet[:1] == "$":
            self.wallet_name = wallet[1:]
        else:
            self.wallet_name = wallet

        self.parse_wallet_name()
        self.resolv()

    def parse_wallet_name(self):
        """ break out the wallet name into its component parts """

        if self.wallet_name[-1] == "/":
            self.wallet_name = self.wallet_name[:-1]

        if self.wallet_name.find("@") >= 0:
            self.coin = self.wallet_name.split("@")[0]
            start_coin = len(self.coin) + 1
        else:
            start_coin = 0
            self.coin = ""

        if self.wallet_name.find("/") >= 0:
            slash = self.wallet_name.split("/")
            if len(slash) > 2:
                raise ValueError("Only one part to the path name is supported")

            self.tag = slash[1]
            self.hostname = self.wallet_name[start_coin:len(self.wallet_name) -
                                             len(self.tag) - 1]
        else:
            self.hostname = self.wallet_name[start_coin:]

        if self.tag == "default":
            self.tag = ""

        if not validation.is_valid_host(self.hostname):
            raise ValueError("Invalid host name")

    def get_doh_data(self):
        """ get dns TXT data for {self.hostname} in DoH format """
        tld = self.hostname.split(".")[-1]

        if tld == "eth":
            return eth.get_eth_txt(self.hostname)

        qry = resolv.Query(self.hostname, "TXT")
        if tld in icann_tlds.tlds:
            qry.servers = servers.icann_servers
        else:
            qry.servers = servers.handshake_servers

        if self.servers is not None:
            qry.servers = self.servers

        return qry.resolv()

    def resolv(self):
        """ get the wallet id from the wallet name """
        ans = self.get_doh_data()

        if "Answer" not in ans:
            raise ValueError(f"No TXT RRs could be found for '{self.hostname}/{self.tag}'")

        for each_ans in ans["Answer"]:
            if each_ans["type"] != TXT_RR_TYPE_ID or each_ans["data"][
                    0:5] != "\"ico ":
                continue

            fields = {
                f.split(":")[0]: f.split(":")[1]
                for f in each_ans["data"][1:-1].split(" ") if f.find(":") >= 0
            }

            if "tag" not in fields or fields["tag"] == "default":
                fields["tag"] = ""

            if fields["tag"] != self.tag:
                continue

            if self.coin == "":
                self.coin = find_coin(fields)

            if self.coin != "" and self.coin in fields:
                validated = ("AD" in ans and isinstance(ans["AD"], bool)
                             and ans["AD"])
                self.wallet_id = {
                    "hostname": self.hostname,
                    "validated": validated,
                    "coin": self.coin,
                    "wallet_name": self.wallet_name,
                    "wallet_id": fields[self.coin]
                }
                if self.tag != "":
                    self.wallet_id["tag"] = self.tag

                return self.wallet_id

        raise ValueError(f"No matching TXT could be found for '{self.hostname}/{self.tag}'")


def run():
    """ main """
    parser = argparse.ArgumentParser(
        description='This is a wrapper to test the wallet code')
    parser.add_argument("-w",
                        "--wallet",
                        default="$btc@jrcs.net",
                        help="Wallet to find")
    parser.add_argument("-s", "--servers", help="Resolvers to query")

    args = parser.parse_args()

    try:
        my_wallet = Wallet(args.wallet, local_servers=args.servers)
        if my_wallet.wallet_id is not None:
            print(json.dumps(my_wallet.wallet_id, indent=2))
        else:
            print(f"ERROR: No wallet named '{args.wallet}' could be found")
    except ValueError as err:  # pylint: disable=broad-except
        print(f"ERROR: {str(err)}")


if __name__ == "__main__":
    run()
