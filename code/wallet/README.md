# Intro

This was tested on Alpine v3.13 with Python v3.8.10 and dnspython v2.0.0

All code is PEP8 & passes `pylint` (with a few minor disables)


# Code to translate a Wallet Name to a Wallet Id

`resolv.py` - resolves a name & rr-type into an DoH JSON object doing DNS over UDP

`eth.py` - uses http://eth.link/ to get DoH records from ETH/DNS

`wallet.py` - takes a wallet name & outputs a JSON object of the wallet id

These three can be run from the command line for debugging.


`ico_flask.py` - a python/flask application to provide wallet lookup as a rest/api

The URL for the api is `/ico/v1/api?name=<wallet-name>`. If you ask for `/ico` or `/ico/v1` you
will get a "hello" JSON.

If you just run `ico_flask.py` it will run a debugging HTTP server on `127.0.0.1`

`wsgi.py` is for use in the micro-server docker container only


# Example

    $ ./wallet.py -w 'btc@jrcs.net/default'
    {
    "hostname": "jrcs.net",
    "validated": true,
    "coin": "btc",
    "wallet_id": "3MU5WsLWqbK6o9buaD4HtXK1KgozcV8BWj"
    }


(if you have any $btc spare, feel free to send me some)


## ICANN TLD List

The file `icann_tlds.txt` lists all the TLDs that should be treated as ICANN TLDs.

Requests for ICANN TLDs will be sent to separate (public) DNS Resolvers to get a faster reply, by default `8.8.8.8` & `1.1.1.1`

Requests for Handshake TLDs are sent to a Handshake Resolver I run - `bridge.jrcs.net`

Requests for ETH/DNS domain are sent to the DoH service run by Cloudflare at http://eth.link/

The destination of these categories of TLD can be tweaked using environment variables.
