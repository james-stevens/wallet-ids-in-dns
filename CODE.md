# The `wallet` module

The module `wallet.py` is provided to look up a wallet name & return `None` or a JSON object of the wallet id & coin type. 
You can test it out using the `tst_wallet.py` wrapper.

When you provide the wallet name, you **must** provide the coin name. The wallet name can optionally have either a `$` or `ico://` prefix.


## NOTE

NOTE: It will trigger an exception if the wallet name records are *NOT* signed with DNSSEC.



# Future

In the furture I will add code to make this work as a micro-service using `nginx` & `flask`



# FYI

This was tested on Alpine v3.13 with Python v3.8.10 and dnspython v2.0.0

All code is PEP8 & passes `pylint` (with a few minor disables)

You can also run `./tst_resolv.py` to test just the DNS lookup part.


# Example

	$ ./tst_wallet.py -w 'btc@jrcs.net/default'
	{
	"coin": "btc",
	"wallet_id": "3MU5WsLWqbK6o9buaD4HtXK1KgozcV8BWj"
	}

