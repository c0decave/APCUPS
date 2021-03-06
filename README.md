# APC UPS/USV

## APCUPSD Information Leak

### What is it?

This script abuses an unauthenticated information leak in the apcupsd daemon. 
The apcupsd daemon is part of the APC UPS/USV chain, it's job is to shutdown or keep your
servers surviving, as long as it has battery power left.

### What information can be gathered?

* Operating System
* Version of APCUPSD
* Battery Status
* SerialNumber
* Firmware Version
* USV Model
* Shutdown times

and some more :)

### How does it work?

The daemon, listening per default at tcp/3551 is waiting for connections. The protocol itself is
build pretty simple. Lets look at the status request:

`\x00\x06\x73\x74\x61\x74\x75\x73`

As you can see, the first two bytes define the length of the request, in this particular case 6 bytes, after that the command is sent: status.


The same is happening for the events request:

`\x00\x06\x65\x76\x65\x6e\x74\x73`

Six bytes again and then the string "events". 
The response is setup similar, first the bytelength, then the ASCII data, at the end a newline and null byte is sent. Finally, if all data has been transfered the daemon sends an additional nullbyte. 

If you looking for more information simply trace wireshark output or look into the code ;)

### Usage

There are two different supported modes in the daemon. Those are:
* status 
* events

While status have detailed information about the daemon and its configuration itself, events covers power failures and alike.

```
./apcupsd_disclosure.py -h
usage: apcupsd_disclosure.py 0.1 dash@undisclose.de June 2019
       [-h] [-m MODE] -t TARGET [-p PORT]

 Lil' tool for Information Disclosure of apcupsd

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  define the mode, two modes exist: "status" and
                        "events", default is "status"
  -t TARGET, --target TARGET
                        define the target
  -p PORT, --port PORT  define the target port
```

Get the status information (you do not need the -m option as status is default):
```
./apcupsd_disclosure.py -t 127.0.0.1 -m status
```

Get the events:
```
./apcupsd_disclosure.py -t 127.0.0.1 -m events
```

### Shodan

Search: https://www.shodan.io/search?query=port%3A3551
Results: 26,000

## Disclaimer

Don't do evil.
