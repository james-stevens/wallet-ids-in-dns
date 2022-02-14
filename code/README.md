# Docker Container

Run `./dkmk` to make a docker container called `ico-wallet` that will provide an HTTPS micro-server
to resolve wallet names into wallet ids. By default it uses a certificate from an private ceritifcate authority
so will not verify, unless you use the `myCA.pem` file to validate the private certificate authority.

If you map or load a Key+Certificate pair PEM into the container at `/opt/pems/certkey.pem`, then `nginx` will use that. This
is so you can use a publicly verifiable certificate of your choice.

If you update the `certkey.pem` file, it will be automatically re-read by `nginx` by checking the date & time
on the file every hour, on the hour.

`ico-wallet.tar.xz` is a `docker image save` of the container, created using the script `dump`.

The container provides an HTTPS service only. The URL for the api is `/ico/v1/api?name=<wallet-name>`.


There is a demo of this container at https://ico.jrcs.net/


## Container Environment Variables

| Variabe Name | Use
| ------------ | ---
| ICO_ICANN_TLDS | file to load the list of ICANN TLDs from (one per line, any order). This file *must* be mapped or loaded into the container, e.g. using `-v`
| ICO_ICANN_EXCLUDE | TLDs that are in the ICANN list that should not be treated as ICANN TLDs. Queries for excluded TLDs are sent to the Handshake Server(s)
| ICO_ICANN_SERVERS | Comma separated list of IP Addresses to send ICANN TLD queries to, using standard DNS over UDP. By default `8.8.8.8` & `1.1.1.1`
| ICO_HANDSHAKE_SERVERS | Comma separated list of IP Addresses to send Handshake TLD queries to, using standard DNS over UDP, by default `109.169.23.69` (`bridge.jrcs.net`)
| ICO_ETH_GATEWAY | URL prefix to send ETH/DNS queries to, by default `eth.link/dns-query`
| ICO_WALLET_SESSIONS | number of service threads per session (for 3 sessions), default=3 (threads)
| ICO_SYSLOG_SERVER | if defined, log to this syslog server, instead of `stdout`


For details on the code itself, see the `wallet` directory.
