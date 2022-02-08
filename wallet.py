#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" translate a <wallet name> into a <wallet id> """

import resolv
import validation

TXT_RR_TYPE_ID = 16


class Wallet:  # pylint: disable=too-few-public-methods
    """ translate a <wallet> name into a wallet id as a JSON, or None """
    def __init__(self, wallet, servers="8.8.8.8,1.1.1.1"):
        self.hostname = None
        self.coin = None
        self.tag = ""
        self.wallet_name = None
        self.wallet_id = None
        self.servers = servers.split(",")

        if wallet[0:6] == "ico://":
            self.wallet_name = wallet[6:]
        elif wallet[:1] == "$":
            self.wallet_name = wallet[1:]
        else:
            self.wallet_name = wallet
        if self.wallet_name[-1] == "/":
            self.wallet_name = self.wallet_name[:-1]

        if self.wallet_name.find("@") < 0:
            raise ValueError("No coin prefix in wallet name")

        self.coin = self.wallet_name.split("@")[0]
        if self.wallet_name.find("/") >= 0:
            slash = self.wallet_name.split("/")
            if len(slash) > 2:
                raise ValueError("Only one part to the path name is supported")

            self.tag = slash[1]
            self.hostname = self.wallet_name[len(self.coin) +
                                             1:len(self.wallet_name) -
                                             len(self.tag) - 1]
        else:
            self.hostname = self.wallet_name[len(self.coin) + 1:]
        if self.tag == "default":
            self.tag = ""

        if not validation.is_valid_host(self.hostname):
            raise ValueError("The hostname in the wallet name is invalid")

    def resolv(self):
        """ get the wallet id from the wallet name """
        qry = resolv.Query(self.hostname, "TXT")
        qry.servers = self.servers
        ans = qry.resolv()
        if "CD" not in ans or not ans["CD"]:
            raise ValueError("CD flag (dnssec) missing or not set")

        if "Answer" not in ans:
            return None

        for each_ans in ans["Answer"]:
            if each_ans["type"] != TXT_RR_TYPE_ID or each_ans["data"][
                    0:5] != "\"ico ":
                continue

            fields = {
                f.split(":")[0]: f.split(":")[1]
                for f in each_ans["data"][1:-1].split(" ") if f.find(":") >= 0
            }

            if "tag" not in fields:
                fields["tag"] = ""

            if fields["tag"] != self.tag:
                continue

            if self.coin in fields:
                self.wallet_id = {
                    "coin": self.coin,
                    "wallet_id": fields[self.coin]
                }
                return self.wallet_id

        return None
