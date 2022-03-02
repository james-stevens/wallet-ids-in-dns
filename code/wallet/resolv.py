#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" module to resolve DNS queries into DoH JSON objects """

from syslog import syslog
import socket
import select
import argparse
import os
import json
import dns
import dns.name
import dns.message
import dns.rdatatype

import validation

DNS_MAX_RESP = 4096
MAX_TRIES = 10
DNS_FLAGS = {
    "QR": 0x8000,
    "AA": 0x0400,
    "TC": 0x0200,
    "RD": 0x0100,
    "AD": 0x20,
    "CD": 0x40,
    "RA": 0x80
}

dohServers = ["8.8.8.8", "8.8.4.4"]
if "DOH_SERVERS" in os.environ:
    dohServers = os.environ["DOH_SERVERS"].split(",")


def resolv_host(server):
    """ resolve {host} to an IP if its a host name """
    if validation.is_valid_ipv4(server):
        return server
    if validation.is_valid_host(server):
        return socket.gethostbyname(server)
    return None


class ResolvError(Exception):
    """ custom error """


class Query:  # pylint: disable=too-few-public-methods
    """ build a DNS query & resolve it """
    def __init__(self, name, rdtype):
        if not validation.is_valid_host(name):
            raise ResolvError(f"Hostname '{name}' failed validation")

        self.name = name
        self.rdtype = rdtype
        self.with_dnssec = True
        self.do = False
        self.cd = False
        self.servers = ["8.8.8.8", "1.1.1.1"]

    def resolv(self):
        """ resolve the query we hold """
        res = Resolver(self)
        return res.recv()


class Resolver:
    """ resolve a DNS <Query> """
    def __init__(self, qry):
        self.qryid = None
        self.reply = None
        if not validation.is_valid_host(qry.name):
            raise ResolvError(f"Hostname '{qry.name}' failed validation")

        if isinstance(qry.rdtype, int):
            rdtype = int(qry.rdtype)
        else:
            rdtype = dns.rdatatype.from_text(qry.rdtype)

        if hasattr(qry, "servers"):
            self.servers = qry.servers
        else:
            self.servers = dohServers

        for each_svr in qry.servers:
            if not validation.is_valid_ipv4(each_svr):
                raise ResolvError("Invalid IP v4 Address for a Server")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.sock is None:
            raise ResolvError("Failed to open UDP client socket")

        self.expiry = 1
        self.tries = 0
        msg = dns.message.make_query(qry.name,
                                     rdtype,
                                     want_dnssec=(qry.do or qry.cd))

        self.question = bytearray(msg.to_wire())

    def send_all(self):
        """ send the query to all servers """
        ret = False
        for each_svr in self.servers:
            try:
                sent_len = self.sock.sendto(self.question, (each_svr, 53))
                ret = ret or (sent_len == len(self.question))
            # pylint: disable=unused-variable,broad-except
            except Exception as err:
                syslog(str(err))

        return ret  # True if at least one worked

    def send(self):
        """ send the DNS query out """
        if self.question is None:
            return None
        self.question[0] = 0
        self.question[1] = 0
        while self.question[0] == 0 and self.question[1] == 0:
            self.qryid = os.urandom(2)
            self.question[0] = self.qryid[0]
            self.question[1] = self.qryid[1]

        return self.send_all()

    def match_id(self):
        """ cehck the DNS quiery Id field matches what we asked """
        return (self.qryid is not None and self.reply[0] == self.qryid[0]
                and self.reply[1] == self.qryid[1])

    def recv(self, binary_format=False):
        """ look for dns UDP response and read it """
        while self.tries < MAX_TRIES:
            if not self.send():
                self.sock.close()
                return None

            while True:
                rlist, _, _ = select.select([self.sock], [], [], self.expiry)
                if len(rlist) <= 0:
                    break

                self.reply, (addr, _) = self.sock.recvfrom(DNS_MAX_RESP)
                if self.match_id():
                    if binary_format:
                        return self.reply

                    if (ret := self.decode_reply()) is None:
                        return None

                    ret["Responder"] = addr
                    self.sock.close()
                    return ret

            self.expiry += int(self.expiry / 2) if self.expiry > 2 else 1
            self.tries += 1

        self.sock.close()
        return None

    def decode_reply(self):
        """ decode binary {message} in DNS format to dictionary in DoH fmt """
        msg = dns.message.from_wire(self.reply)
        if (msg.flags & DNS_FLAGS["QR"]) == 0:
            return None  # REPLY flag not set

        out = {}

        for flag in DNS_FLAGS:
            out[flag] = (msg.flags & DNS_FLAGS[flag]) != 0

        out["Status"] = msg.rcode()

        out["Question"] = [{
            "name": rr.name.to_text(),
            "type": rr.rdtype
        } for rr in msg.question]

        out["Answer"] = [{
            "name": rr.name.to_text(),
            "data": i.to_text(),
            "type": rr.rdtype
        } for rr in msg.answer for i in rr]

        out["Authority"] = [{
            "name": rr.name.to_text(),
            "data": i.to_text(),
            "type": rr.rdtype
        } for rr in msg.authority for i in rr]

        return out


def main():
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
    else:
        qry = Query(args.name, args.rdtype)
        qry.servers = args.servers.split(",")
        qry.do = True
        print(json.dumps(qry.resolv(), indent=2))


if __name__ == "__main__":
    main()
