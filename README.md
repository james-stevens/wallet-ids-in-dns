# Proposal for publishing crypto wallet ids in DNS

# Introduction

DNS was created top provide a way to attach a human-readable name to a piece of technical data. Crypto Wallet Ids seem to fit this model.

In the past it has been common to use custom DNS records types for different data records, but approval can takes ages and updating the infrastructure takes time, so more recently the use of `TXT` records has been preferred.

The aim is to be able to move from something like "please pay `btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m`" to something more like "please pay `my-name.tld`"

By storing the wallets in DNS `TXT` records, it should be possible to store them in a variety of different DNS infrastructures such as the Handshake Blockchain, the ETH/DNS blockchain or any standard DNS zone file.


## Inspiration ##
A previous proposal was published by [Mattias Geniar](https://ma.ttias.be/proposal-cryptocurrency-addresses-dns/), which seems pretty reasonable to me, so I've taken inspiration from it.

In his proposal, Mattias Geniar suggests including a numeric `priority` field, similar to an `MX` record. Although interesting, I think it would be more useful to have a text string "tag" to make it easier to direct people to different wallet ids, with the option of no tag to indicate that to be a default wallet.

## Proposal ##

### Security ###

In order to ensure your wallet ids can not be tampered with (e.g. DNS poisoning), when storing your wallet ids in standard DNS zone data, it is **highly** recommended that the DNS zone that stores your wallet ids is signed, using DNSSEC. That way the client can cryptographically validate the data.

If the records are being stored in a blockchain backed DNS technology, this is not required / relevant.


### DNS Storage Format ###

In DNS the wallet ids will be stored as a `TXT` records with three parts
1. A record identifier to indicate this is a wallet id, for example `ico` (as per Mattias Geniar suggestion) or `wid` (Wallet id). 
2. An option tag in the form `tag:[name]` where `name` conforms to the requirement of a DNS hostname, i.e. a string of up to 63 characters of upper or lower case letters, numbers & hyphen, including support for encoding UTF-8 using [Punycode](https://en.wikipedia.org/wiki/Punycode). No tag or a tag with the reserved word `default` will indicate this is the default wallet for a particular currency.
3. A wallet id, prefixed by the three character cryptocurrency identifier ("btc", "eth", "hns", etc)

For example

    my-name.tld. 86400 IN TXT "ico tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    my-name.tld. 86400 IN TXT "ico ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"
    my-name.tld. 86400 IN TXT "ico tag:business btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"
    my-name.tld. 86400 IN TXT "ico tag:biz btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"


Where multiple wallet ids exist for the same currency, with the same tag, which actual wallet is selected is client-dependant, so should be avoided.

Any host name can be used as a holder of a wallet id, so the following would be equally valid

    wallet.my-name.tld. 86400 IN TXT "ico tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    wallet.my-name.tld. 86400 IN TXT "ico tag:default ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"


Host names that have a `CNAME` should be followed to the target host.

    cash.name.tld. 86400 IN CNAME wallet.my-name.tld.


If, instead of using a single host name & using `tags`, you store each wallet id in a different host name this will slightly improve privacy, but not a lot. For example,

    my-name.tld. 86400 IN TXT "ico btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    my-name.tld. 86400 IN TXT "ico ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"
    business.my-name.tld. 86400 IN TXT "ico btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"
    biz.my-name.tld. 86400 IN TXT "ico btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"


### Wallet Name Format ###

Wallet names can then be defined in the same style as URLs, with the record identifier (see above) as the protocol field, the host name in the host name field and the tag as the path. With the currency as an optional prefix to the host name followed by `@`. So the full URL for these wallets would be

    ico://btc@my-name.tld/
    ico://ltc@my-name.tld/
    ico://btc@my-name.tld/business
    ico://btc@my-name.tld/biz

In many circumstances the context of the information will make the prefix of the protocol, &/or currency, unnecessary. So "please pay me in bitcoin at `my-name.tld`" or "please pay `btc@my-name.tld`" can make make the one or two prefixes unnecessary.


## Storing A Wallet in a TLD Zone ##

If you only wish to use a domain name as a wallet identifier, then it could be possible to store the wallet's `TXT` records in the upper level zone file. This has the advantage, to the owner, of meaning they do not need to provide/run any infrastrucutre to give their wallets a name.

As most domain registration is done using the `EPP` protocol, and there is no `EPP` extension for this, this proposal suggests a work-around that enables existing domain name registration software to support this.

To achieve this, it is proposed that the name server (`NS`) records specified for the domain name have a special prefix that indicates they should be read as wallet ids. These are effectively "fake" `NS` records, as the registry will be require to translate them into `TXT` records, as above.

So this proposal is the fake `NS` consist of the following parts
1. The fixed identification prefix, for example `zz--wallet`
2. An optional tag
3. The cryptocurrency identifier
4. The wallet identifier
5. The domain name these wallets are being registered in

So, for example, if we have just registered the domain name `my-name.tld` and we wish to **only** use it as a crypto wallet identification, we could specify the follow fake `NS` records to achieve the wallet set up above

    zz--wallet.btc.1AeCyEczAFPVKkvausLSQWP1jcqkccga9m.my-name.tld.
    zz--wallet.ltc.Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW.my-name.tld.
    zz--wallet.business.ltc.Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW.my-name.tld.
    zz--wallet.biz.ltc.Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW.my-name.tld.

Once these have been parsed by the registry, they would create the following `TXT` records.

    my-name.tld. 86400 IN TXT "ico tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"
    my-name.tld. 86400 IN TXT "ico tag:default ltc:Lh1TUmh2WP4LkCeDTm3kMX1E7NQYSKyMhW"
    my-name.tld. 86400 IN TXT "ico tag:business btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"
    my-name.tld. 86400 IN TXT "ico tag:biz btc:SQWP1jcqkccga9m1AeCyEczAFPVKkvausL"

The advantage, to the owner, of supporting this functionality in the registry is that
1. The wallets ids will resolve and validate quicker
2. The registry is already publishing & signing the DNS, so the owner does not need to run any additional servers or services

If you wish to use your domain name as **both** a DNS domain name and a cryptocurrency wallet identifier, then you will need to use a DNS hosting provider & point real (not fake) `NS` records to your hosting provider in the normal way. Then create all your records within the zone on your DNS hosting provider.
