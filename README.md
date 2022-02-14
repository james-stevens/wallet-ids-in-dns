# Giving Your Crypto Wallet a Name, using DNS

# Introduction

DNS was created to provide a way to attach a human-readable name to a piece of technical data. Crypto Wallet Ids seem to fit this model.

In the past it has been common to use custom DNS records types for different data records, but approval can takes ages and updating the infrastructure takes even longer, so more recently the use of `TXT` records has been preferred.

The aim is to be able to move from something like "please pay `btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m`" to something more like "please pay `my-name.tld`"

By storing the wallets in DNS `TXT` records, it should be possible to store them in a variety of different DNS infrastructures such as the Handshake Blockchain, the ETH/DNS blockchain or any standard DNS zone file.

I am fully aware of the [HIP-0002](https://hsd-dev.org/HIPs/proposals/0002/) proposal, I just felt it has quite a lot of prerequisites, so creates quite a high barrier to entry. I wanted to propose something much simpler & easier to set-up. For example, `DANE` validation is significanly more complex to set up and validate. It will also take longer to both retrieve & validate than my proposal. The proposal also doesn't seem to describe various areas of functionality I felt needed flashing out.



## Inspiration
A previous proposal was published by [Mattias Geniar](https://ma.ttias.be/proposal-cryptocurrency-addresses-dns/), which seems pretty reasonable to me, so I've taken inspiration from it.

In his proposal, Mattias Geniar suggests including a numeric `priority` field, similar to an `MX` record. Although interesting, I think it would be more useful to have a text string "tag" to make it easier to direct people to different wallet ids, with the option of no tag to indicate that to be a default wallet.


# Proposal

## Wallet Name Format

Wallet names are defined in the same style as URL in the form `<idenifier>`://`[ <currency>@ ]<dns-name>[ /<tag>]`

So the record identifier (the fixed string `ico`) in the protocol field, the DNS name in the host name field and the `tag` as the path. With the currency as an optional prefix to the host name followed by `@`. So the full URL for our exmaple wallets would be

    ico://btc@my-name.tld/
    ico://ltc@my-name.tld/
    ico://btc@my-name.tld/business
    ico://btc@my-name.tld/biz

In many circumstances the context of the information will make the prefix of the protocol, &/or currency, unnecessary. So "please pay me in bitcoin at `my-name.tld`" or "please pay `btc@my-name.tld`" can make make the one or two prefixes unnecessary, or (for exmaple) if you are specfying a wallet on an auction site that only holds auctions in `eth`, then the `eth@` prefix is redundant.

Where there may be confusion between the shortened version and an email address, but the user prefers to not use the full URL style format, prefixing the cryptocurrency name with a dollar (`$`) sign can be used to clarify that this is a crypto wallet name. For example, `$btc@my-name.tld` or `$my-name.tld`. The dollar sign prefix should not be used when specifying the full URL format - `ico://....`.



## DNS Storage Format

In DNS the wallet ids will be stored as a `TXT` records with three parts
1. A record identifier to indicate this is a wallet id, for example `ico` (as per Mattias Geniar suggestion) or `wid` (Wallet id). 
2. An option tag in the form `tag:[name]` where `name` conforms to the requirement of a DNS hostname, i.e. a string of up to 63 characters of upper or lower case letters, numbers & hyphen, including support for encoding UTF-8 using [Punycode](https://en.wikipedia.org/wiki/Punycode). No tag or a tag with the reserved word `default` will indicate this is the default wallet for a particular currency.
3. A wallet id, prefixed by the three character cryptocurrency identifier ("btc", "eth", "hns", etc)

When tags are searched for a matching tag, the search should be case insensitive, so it would be permissible to fold tags to lowercase. For a client searching for a matching tag, if they have been given no tag or the tag `default`, then this should either match `TXT` records with no tag or with the tag `default`. However, if a tag was provided and no matching tag has been found, and the tag is NOT `default`, then the client should NOT fall back to matching the default tag, but instead give an error.

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


### Notes to Crypto Wallet Hosting Providers

It should be relatively trivial for wallet hosting providers to automatically (or optionally) publish their client's wallet ids in this format. They can either do this in their main domain name, or in a separate domain registered for the purposes.

It is **highly** recommended that they do NOT use the user's account name as any part of the wallet name, as this could present an unnecessary security risk. Instead they could offer the client to provide a "nickname" for their wallet that can be unrelated to the client's login credentials.

The wallet hosting provider can then publish the wallet ids in one of two formats

        nickname.provider.tld. 86400 IN TXT "ico btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"

or

        provider.tld. 86400 IN TXT "ico tag:nickname btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"

Each will give the client's wallet a slightly different name. The wallet hosting provider will have to choose which they prefer, or use some other format within the scope of this specification. If they use the first format, they must ensure the client's chosen nicknames do not clash with hostnames they are using for technical putposes, e.g. `www`.




### Some Basic DNS Rules You Need to Know

There are two basic DNS rules you may need to know.

#### 1. The CNAME Rule

If a `CNAME` record exists for a host, **NO** other records of any type can exist for that host name. A `CNAME` is like an alias to another host name, so all data must exist at the destination host name, no data can exist at the `CNAME`.

         cash.name.tld. 86400 IN CNAME wallet.my-name.tld.

In this example, the name `cash.name.tld` can **ONLY** have a `CNAME`, so any `TXT` records must exist at the destination host, in this example `wallet.my-name.tld`.


#### 2. The NS Rule

If a domain has `NS` records it is defined as a sub-domain. All data for the sub-domain can only exist in the zone file for the sub-domain. The only other permitted record type in the parent zone is `DS`, which is used to validate DNSSEC. Any other records types in the parent zone will be silently ignored. In circumstances crcumstances IP Address records can exist, but they **MUST** also be repeated in the sub-domain's zone file.

For example

        example. 86400 IN NS ns1.example.
        example. 86400 IN TXT "ico tag:default btc:1AeCyEczAFPVKkvausLSQWP1jcqkccga9m"

In this case the `NS` record defines `example.` as a sub-domain, so the `TXT` record will be silently ignored and instead be placed in the DNS records for the sub-domain. But in this example, IP Addresses records for `ns1.example.` should be provided, but the `NS` records & IP Address records **MUST** also be repeated in the sub-domain data for `example.`.



### DNS and Security

In order to ensure your wallet ids can not be tampered with (e.g. DNS poisoning), when storing your wallet names & ids in standard DNS zone data, it is **highly** recommended that the DNS zone that stores your wallet ids is signed, using DNSSEC. That way the client can cryptographically validate the data.

If the records are being stored in a blockchain backed DNS technology, this is not required / relevant.


# Storing A Wallet in a TLD Zone

If you only wish to use a domain name as a wallet identifier, then it could be possible to store the wallet's `TXT` records in the upper level zone file. This has the advantage, to the owner, of meaning they do not need to provide/run any infrastrucutre to give their wallets a name.

As most domain registration is done using the `EPP` protocol, and there is no `EPP` extension for this, this proposal suggests a work-around that enables existing domain name registration software to support this.

To achieve this, it is proposed that the name server (`NS`) records specified for the domain name have a special prefix that indicates they should be read as wallet ids. These are effectively "fake" `NS` records, as the registry will be require to translate them into `TXT` records, as above.

So this proposal is the fake `NS` consist of the following parts
1. The fixed identification prefix, for example `zz--wallet`
2. An optional tag
3. The cryptocurrency identifier consisiting of three alphabetic characters. This can be folded to lower case.
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

Each part of a DNS hostname can be up to 63 characters. If a wallet id is longer than 63 characters, it can be split using a period (`.`). This should be automatically detected by the registry and the id should be reformed into a single string, omitting the period, before the wallet id is put into the `TXT` record.



### HEX vs BASE64 formats

Cryptocurrency Wallet Ids come in one of two formats, `base64` and `hex`. Base64 ids will be numbers and mixed upper & lower case letter and NOT have an `0x` prefix. Hex ids will start with the prefix `0x` and consist of numbers and the letters `A` to `F` (or `a` to `f`) only. Hex ids are NOT case sensitive, base64 ids ARE case sensitive. They are essentially just different formats for representing the same information as the underlying wallet id is actually binary.

DNS specifications state that DNS host names can be mixed case and that the case of the lettering must be retained, but that host names should be searched for ignoring the case. This case insensitive search requirement can lead to some DNS software folding all names to lower case to make searches faster. Technically this is incorrect, but it can be quite common.

Therefore, if you are using these kinds of "fake" `NS` records to communicate wallet ids to a registry, is is recommended that they are always communicated in `HEX` format, as this is NOT case sensitive. 

It should be possible for a registrar, that supports this specification, to store wallet ids in either `base64` or `hex` format, but convert them to `hex` format for the purposes of communicating them to the registry. Although the end user may find it easier to only specify `hex` in the first place, as this might make it easier for them to check their wallet ids have been communicated to the registry correctly.


### Notes to registrars

Domain Name Registrars that want to support this functionality should provide their clients with a user interface that knows about, stores & prompts the users for wallet ids & cryptocurrencies, instead of requiring the user to know about this specification and make the `TXT` records themselves.



# Advice to Clients

Client software & UI/UX's wishing to make a payment can now do a simple DNS lookup to retrieve the wallets ids of the person to be paid. This should be done at the time the payer enters the address, so they know immediately if a wallet id can be found for the wallet address they have just given.

Where a wallet tag has been specified, but can not be found, the client should not fall back to any default wallet (if present), but instead present the payer with an error message. DNS is usually sufficiently fast that it should be relatively trivial to do a look up live.

Where no `TXT` records exist for the wallet name given, payers should also be warned at the time the wallet name is presented.

All clients should support accepting wallet names in full unicode format, allowing for the full range of unicode characters, then automatically convert the host name & (optional) tag into punycode. It is likely accepting the user's input in UTF-8 will be the most convenient for this. Library code for doing a UTF-8 to punycode conversion is available in many development environments / programming languages.

If a wallet name is supplied that excludes a coin name, the client should select any one with a matching hostname and (optional) tag. Where more than one matching wallet name exists, which the client selects is not determined, so this should be avoided.


# Reserve Wallet Id Lookup

DNS provides a mechanism for both forward & reverse lookup for host names & their IP Addresses. That is, if you know a host name you can lookup an IP Address, and if you know an IP Address you can look up a hostname.

This proposal suggests a way to know a wallet name & look up a wallet id / address. It might be nice to have a facility to know a wallet id & lookup a wallet name. For example, so you can get a wallet name of somebody who just paid you.

This would require a single jump-off point for the look-up & somebody to run that. Therefore, although this may be desirable, this is considered outside of the scope of this document, for the time being.
