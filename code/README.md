# The `wallet` module

The module `wallet.py` is provided to look up a wallet name & return `None` or a JSON object of the wallet id & coin type. 
It has its own `main()` so you can test it by just running it.

When you provide the wallet name, you **must** provide the coin name. The wallet name can optionally have either a `$` or `ico://` prefix.



# Future

In the furture I will add code to make this work as a micro-service using `nginx` & `flask`



# FYI

This was tested on Alpine v3.13 with Python v3.8.10 and dnspython v2.0.0

All code is PEP8 & passes `pylint` (with a few minor disables)

You can also run `./resolv.py` to test just the DNS lookup part.


# Example

	$ ./wallet.py -w 'btc@jrcs.net/default'
	{
	"hostname": "jrcs.net",
	"validated": true,
	"coin": "btc",
	"wallet_id": "3MU5WsLWqbK6o9buaD4HtXK1KgozcV8BWj"
	}


(if you have any $btc spare, feel free to send me some)


# Docker Container

Run `./dkmk` to make a docker container called `ico-wallet` that will provide an HTTPS micro-server
to resolve wallet names into wallet ids. By default it uses a certificate from an private ceritifcate authority
so will not verify, unless you use the `myCA.pem` file to validate the private certificate authority.

If you map a Key+Certificate pair into the file `/opt/certkey.pem`, then `nginx` will use that. This
is do you can use a verifiable certiifcate of your choice.

If you update the `certkey.pem` file, it will be automatically re-read by `nginx` by check the date & time
one the file every hour.

`ico-wallet.tar.xz` is a `docker image save` of the container, created using the script `dump`.

The container provides an HTTPS service only.


## Container Environment Variables

`ICO_ICANN_TLDS` - file to load the list of ICANN TLDs from (one per line, any order). This file *must* be mapped or loaded into the container, e.g. using `-v`

`ICO_ICANN_EXCLUDE` - TLDs that are in the ICANN list that should not be treated as ICANN TLDs

`ICO_ICANN_SERVERS` - Comma separated list of IP Addresses to send ICANN TLD queries to, using standard DNS over UDP. By default `8.8.8.8` & `1.1.1.1`

`ICO_HANDSHAKE_SERVERS` - Comma separated list of IP Addresses to send Handshake TLD queries to, using standard DNS over UDP, by default `109.169.23.69` (`bridge.jrcs.net`)

`ICO_ETH_GATEWAY` - URL prefix to send ETH/DNS queries to, by default `eth.link/dns-query`

`ICO_SESSIONS` - number of service sessions, default=5

`ICO_SYSLOG_SERVER` - if defined, log to this syslog server, instead of `stdout`
