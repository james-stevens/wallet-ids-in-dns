# Giving Your Crypto Wallet a Name, using DNS

# Introduction

DNS was created to provide a way to attach a human-readable name to a piece of technical data.
Crypto Wallet Ids seem to fit this model.

In the past it has been common to use custom DNS records types for different data types,
but approval can takes ages and updating the infrastructure takes even longer, so more
recently the use of hostname prefixes and `TXT` records has been preferred.

The aim is to be able to move from something like "please pay `btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m`"
to something more like "please pay `my-name.tld`"

By storing the wallets in DNS `TXT` records, it should be possible to store them in a variety of
different DNS infrastructures such as the Handshake Blockchain, the ETH/DNS blockchain or any (ICANN) standard DNS zone file.

I am fully aware of the [HIP-0002](https://hsd-dev.org/HIPs/proposals/0002/) proposal, I just
felt it has quite a lot of prerequisites, so creates quite a high barrier to entry. I wanted
to propose something much simpler & easier to set-up.
Most Domain Name Registrars offer DNS hosting as part of their domain name service, so a pure DNS solution is more accessible.

HIP-0002 will also take longer to both retrieve & validate than a pure DNS solution
and proposal also doesn't seem to describe various areas of functionality I felt needed flashing out.



## Inspiration
A previous proposal was published by [Mattias Geniar](https://ma.ttias.be/proposal-cryptocurrency-addresses-dns/),
which seems pretty reasonable to me, so I've taken a lot of inspiration from it.

In his proposal, Mattias Geniar suggests including a numeric `priority` field,
similar to an `MX` record. Although interesting, I think it would be more useful to have
a text string "tag" to make it easier to direct people to different wallet ids, with the
option of no tag to indicate that to be a default wallet.


# Proposal

## Wallet Name Format

Wallet name presentation format is defined in the style of a URI in the form `<idenifier>`://`[ <currency>@ ]<dns-name>[ /<tag>]`

The record identifier is the fixed string `ico`, in the protocol field. The host name field is the DNS hostname, less the `_ico.` prefix
and the `tag` as the path. With the currency as an optional prefix to the host name followed by `@`.
So the full URI for some exmaple wallets could be

    ico://my-name.tld/
    ico://ltc@my-name.tld/
    ico://btc@my-name.tld/business
    ico://btc@my-name.tld/biz

In many circumstances the context of the information will make the prefix of the protocol,
&/or currency, unnecessary. So "please pay me in bitcoin at `my-name.tld`"
or "please pay `btc@my-name.tld`" can make make the one or two prefixes unnecessary.
If you are specfying a wallet on an auction site that only holds auctions
in `eth`, then specifying an `eth@` prefix becomes redundant.

Where there may be confusion between the shortened version and an email address, but the
user prefers to not use the full URI style format, prefixing the cryptocurrency name with
a dollar (`$`) sign can be used to clarify that this is a crypto wallet name.

For example, `$btc@my-name.tld` or `$my-name.tld`. The dollar sign prefix should not be
used when specifying the full URI format - `ico://....`.



## DNS Storage Format

In DNS the wallet ids will be stored as a `TXT` records with up to three parts

1. A hostname plus the prefix `_ico.` to indicate this is a wallet id.

2. An option tag in the form `tag:[name]` where `name` conforms to the requirement of a DNS hostname,
	i.e. a string of up to 63 characters of upper or lower case letters, numbers & hyphen, including support for encoding UTF-8 using [Punycode](https://en.wikipedia.org/wiki/Punycode).
	No tag, or a tag with the reserved word `default`, will indicate this is the default wallet for a particular currency.

3. A wallet id, prefixed by the three character cryptocurrency identifier, in lower case ("btc", "eth", "hns", etc)

NOTE: the `_ico.` prefix will *ALWAYS* be removed when using the host name in an `ico://` URI, with or without the `ico://` prefix.

When tags are searched, for a matching tag, the search should be case insensitive.
For a client searching for a matching tag, if they have been given no tag or the tag `default`, then this should either match
records with no tag or with the tag `default`.

If a tag was provided and no matching tag has been found, and the tag is NOT `default`,
then the client *MUST NOT* fall back to matching the default tag, but instead give an error.


For example

    _ico.my-name.tld. 86400 IN TXT "tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    _ico.my-name.tld. 86400 IN TXT "ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"
    _ico.my-name.tld. 86400 IN TXT "tag:business btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"
    _ico.my-name.tld. 86400 IN TXT "tag:biz btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"


Where multiple wallet ids exist for the same currency, with the same tag, which actual wallet
is selected is client-dependant, so should be avoided.


Any host name, with a `_ico.` prefix, can be used as a holder of a wallet id, so the following would be equally valid

    _ico.wallet.my-name.tld. 86400 IN TXT "tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    _ico.wallet.my-name.tld. 86400 IN TXT "tag:default ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"


Host names that have a `CNAME` should be followed to the target host.

    _ico.cash.name.tld. 86400 IN CNAME _ico.wallet.my-name.tld.


Instead of using a single host name, & using `tags`, you could store each wallet id in a different host name
this will slightly improve privacy, but not a lot. For example,

    _ico.my-name.tld. 86400 IN TXT "ico btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    _ico.my-name.tld. 86400 IN TXT "ico ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"
    _ico.business.my-name.tld. 86400 IN TXT "ico btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"
    _ico.biz.my-name.tld. 86400 IN CNAME _ico.business.my-name.tld.

So the URI `ico://btc@my-name.tld/business` has become `ico://btc@business.my-name.tld/`



### Notes to Crypto Wallet Hosting Providers

It should be relatively trivial for wallet hosting providers to automatically (or optionally)
publish their client's wallet ids in this format. They can either do this in their main domain name,
or in a separate domain registered for the purposes.

It is **highly** recommended that they do NOT use the user's account name as ANY part of
the wallet name, as this could present an unnecessary security risk. Instead they could
offer the client to provide a "nickname" for their wallet that can be unrelated to the
client's login credentials.

The wallet hosting provider can then publish the wallet ids in one of two formats

	_ico.nickname.provider.tld. 86400 IN TXT "ico btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"

or

	_ico.provider.tld. 86400 IN TXT "ico tag:nickname btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"

These examples would give the client's wallet the names

	ico://btc@nickname.provider.tld/

or

	ico://btc@provider.tld/nickname

(where the `btc@` prefix would be optional, if this was the client's only wallet)

If they use the first format, they must ensure the client's chosen nicknames do not clash with
hostnames they may be using for technical putposes, e.g. `www`.



### Some Basic DNS Rules You Need to Know

There are two basic DNS rules you may need to know.

#### 1. The CNAME Rule

If a `CNAME` record exists for a host, **NO** other records of any type can exist for that host name.
A `CNAME` is like an alias to another host name, so all data must exist at the destination host name,
no other data can exist at the `CNAME`.

	_ico.cash.name.tld. 86400 IN CNAME _ico.wallet.my-name.tld.

In this example, the name `_ico.cash.name.tld` can **ONLY** have a `CNAME`, so any `TXT`
records must exist at the destination host, in this example `_ico.wallet.my-name.tld`.


#### 2. The NS Rule

If a domain has `NS` records it is defined as a sub-domain. All data for the sub-domain
can only exist in the zone file for the sub-domain. The only other permitted record type
in the parent zone is `DS`, which is used to validate DNSSEC.

Any other records types in
the parent zone will be silently ignored. In special crcumstances IP Address records
can exist, but they **MUST** also be repeated in the sub-domain's zone file.

For example

	example. 86400 IN NS ns1.example.
	example. 86400 IN TXT "ico tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"

In this case the `NS` record defines `example.` as a sub-domain, so the `TXT` record will
be silently ignored and instead *MUST* be placed in the DNS data (zone file) for the sub-domain.

But in, this example, IP Addresses records for `ns1.example.` should be provided, but the `NS`
records & IP Address records **MUST** also be repeated in the sub-domain data for `example.`.



### DNS and Security

In order to ensure your wallet ids can not be tampered with (e.g. DNS poisoning),
when storing your wallet names & ids in standard DNS zone data, it is **highly**
recommended that the DNS zone that stores your wallet ids is signed, using DNSSEC.
That way the client can cryptographically validate the wallet ids they received are the ones you entered.

If the records are being stored in a blockchain backed DNS technology, this may not be required / relevant.



### Notes to registrars

Domain Name Registrars that want to support this functionality should provide their clients
with a user interface that knows about, stores & prompts the users for wallet ids & cryptocurrencies,
instead of requiring the user to know about this specification and make the `TXT` records themselves.



# Advice to Clients

Client software & UI/UX's wishing to make a payment can now do a simple DNS lookup to retrieve
the wallets ids of the person to be paid. This should be done at the time the payer enters
the address, so they know immediately if a wallet id can be found for the wallet address they have just given.

Where a wallet tag has been specified, but can not be found, the client should not fall back
to any default wallet (if present), but instead present the payer with an error message.
DNS is usually sufficiently fast that it should be relatively trivial to do a look up live.

Where no `TXT` records exist for the wallet name given, payers should also be warned at
the time the wallet name is presented.

All clients should support accepting wallet names in full unicode format, allowing for the
full range of unicode characters, then automatically convert the host name & (optional) tag
into punycode. It is likely accepting the user's input in UTF-8 will be the most convenient for this.
Library code for doing a UTF-8 to punycode conversion is available in many development environments / programming languages.

If a wallet name is supplied that excludes a coin name, the client should select any one
with a matching hostname and (optional) tag. Where more than one matching wallet name exists,
which the client selects is not determined, so this should be avoided.

If the payee has signed their zone with DNSSEC the client SHOULD do DNSSEC validation. If this validation 
fails the payment *MUST NOT* be made, and the client should give the user an appropriate error message.


# Reverse Wallet Id Lookup

DNS provides a mechanism for both forward & reverse lookup for host names & their IP Addresses.
That is, if you know a host name you can lookup an IP Address, and if you know an IP Address you can look up a hostname.

This proposal suggests a way to know a wallet name & look up a wallet id / address.
It might be nice to have a facility to know a wallet id & lookup a wallet name.
For example, so you can get a wallet name of somebody who just paid you.

This would require a single jump-off point for the look-up & somebody to run that.
Therefore, although this may be desirable, this is considered outside of the scope of this document, for the time being.
