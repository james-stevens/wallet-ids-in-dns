# Code to translate a Wallet Name to a Wallet Id

`resolv.py` - resolves a name & rr-type into an DoH JSON object

`eth.py` - uses http://eth.link/ to get DoH records from ETH/DNS

`wallet.py` - takes a wallet name & outputs a JSON object of the wallet id

`ico_flask.py` - a python/flask application to provide wallet lookup as a rest/api

The first three of these are modules to be called by the fourth, but all can be run from
the command line for debugging.


The URL for the api is `/ico/v1/api?name=<wallet-name>`. If you ask for `/ico` or `/ico/v1` you
will get a "hello" JSON.

If you just run `ico_flask.py` it will run a debugging HTTP server on `127.0.0.1`

`wsgi.py` is for use in the micro-server docker container only



## ICANN TLD List

The file `icann_tlds.txt` lists all the TLDs that should be treated as ICANN TLDs.

Requests for ICANN TLDs will be send to separate publi DNS Resolvers to get a faster reply

Requests for Handshake TLDs are sent to a Handshake Resolver I run

Requests for ETH/DNS domain are sent to http://eth.link/

The destination of these categories of TLD can be tweaked using environment variables.
