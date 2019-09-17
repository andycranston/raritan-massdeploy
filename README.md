# Utility to create the necessary files for a Raritan mass deployment via USB keys or DHCP+TFTP

The `massdeploy.py` utility creates the files needed for a Raritan mass deployment via USB keys or
using the network based DHCP+TFTP method.

By creating and maintaining just one configuration file called:

```
massdeploy.txt
```

the `massdeploy.py` utility generates the following required files:

```
fwupdate.cfg
config.txt
devices.csv
```

which can then be copied to one or more USB keys or can be copied to a TFTP server.

# A demonstration video of `massdeploy.py`

The following link:

[Using the massdeploy.py utility](https://www.youtube.com/watch?v=SOMECODEHERE)

is an introduction to the `massdeploy.py` utility.

## Why use `massdeploy.py` utility instead of the Raritan supplied solution?

Raritan supply the following:

[Spreadsheet for firmware update and configuration mass deployment](http://cdn.raritan.com/download/px2/version-3.5.0/Mass_Deployment_3.5.0_45371.xls)

You load this spreadsheet into Microsoft Excel, ensures Excel macros are enabled, fill in the details
on the second and third sheet and click a button to have the macros generate the `fwupdate.cfg`,
`config.txt` and `devices.csv` files.

Please take a look at this solution because:

* It is a great introdution to the Raritan mass deployment methodology.
* It could be exactly what you need.

If, however, you are interested in a solution that uses one simple configurartion file then read on.

## Prerequisites

You will need a Windows or UNIX/Linux environment with a Python 3 interpreter.  Almost all modern Linux
distributions come bundled with Python 3.  For Windows download Python 3 from here:

[Python Releases for Windows](https://www.python.org/downloads/windows/)

## The `massdeploy.txt` file format

When the `massdeploy.py` utility is run it looks for a file called:

```
massdeploy.txt
```

At a high level the content of this file is split into three sections.  The first section contains the
lines that should go into the `fwupdate.cfg` file.  The second section contains the lines that
should go into the `devices.csv` file and the third and last section contains the lines that go
into the `config.txt` file.

The three sections are separated by a special line that looks like:

```
%%
```

As an example here is a basic `massdeploy.txt` file:

```
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
%%
PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
PK60860023,00:0d:5d:07:6a:85,pdu4,192.168.8.23,24
PK60867390,00:0d:5d:7b:8f:9c,pdu5,192.168.8.24,24
PK60867769,00:0d:5d:23:91:7a,pdu6,192.168.8.25,24
PK60861021,00:0d:5d:89:3a:37,pdu7,192.168.8.26,24
PK60863094,00:0d:5d:03:4c:1b,pdu8,192.168.8.27,24
PK60863926,00:0d:5d:8e:44:2e,pdu9,192.168.8.28,24
PK60867901,00:0d:5d:aa:b7:07,pdu10,192.168.8.29,24
%%
pdu.name=${3}
net.interfaces[eth0].ipv4.enabled=1
net.interfaces[eth0].ipv4.config_method=static
net.interfaces[eth0].ipv4.static.addr_cidr.addr=${4}
net.interfaces[eth0].ipv4.static.addr_cidr.prefix_len=${5}
net.interfaces[eth0].ipv6.enabled=0
```

Assume this `massdeploy.txt` file and the `massdeploy.py` file have been copied to
a directory called `c:\massdeploy` on a Windows system.

Now open a command prompt window and type:

```
c:
cd \massdeploy
python massdeploy.py
```

The following files will now be created:

```
fwupdate.cfg
config.txt
devices.csv
```

The `fwupdate.cfg` file will contain:

```
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
```

The `config.txt` file will contain:

```
PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
PK60860023,00:0d:5d:07:6a:85,pdu4,192.168.8.23,24
PK60867390,00:0d:5d:7b:8f:9c,pdu5,192.168.8.24,24
PK60867769,00:0d:5d:23:91:7a,pdu6,192.168.8.25,24
PK60861021,00:0d:5d:89:3a:37,pdu7,192.168.8.26,24
PK60863094,00:0d:5d:03:4c:1b,pdu8,192.168.8.27,24
PK60863926,00:0d:5d:8e:44:2e,pdu9,192.168.8.28,24
PK60867901,00:0d:5d:aa:b7:07,pdu10,192.168.8.29,24
```

The `devices.csv` file will contain:

```
pdu.name=${3}
net.interfaces[eth0].ipv4.enabled=1
net.interfaces[eth0].ipv4.config_method=static
net.interfaces[eth0].ipv4.static.addr_cidr.addr=${4}
net.interfaces[eth0].ipv4.static.addr_cidr.prefix_len=${5}
net.interfaces[eth0].ipv6.enabled=0
```

Using the `massdeploy.txt` utility in this fashion provides a handy way to
keep the configuration details all in one file.

However there is more...

## Comments

Any line in the `massdeploy.txt` file which begins with the character '#'  is treated as
a comment and is NOT copied into any of the three configuration files.

So, for example, if the start of the `massdeploy.txt` file now begins:

```
#
# massdeploy.txt
#
# version 007 - 16-september-2019
#
# PDUs in data hall 7, first floor
#
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
%%
PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
   ...
   ...
   ...
```

Then those first few lines beginning with the '#' character are ignored by the
`massdeploy.py` utility but remain very helpful in keeping track of things.

Another benefit of the comment system is to temporarily 'comment out' lines.  For example
if the first PDU has already been configured and you do not want it changed you could edit
the `massdeploy.txt` file like this:

```
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
%%
# PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
   ...
   ...
   ...
```

## Easier ${} substitution

In the third config section of the `massdeploy.txt` file the ${} substitution technique is
used to refer to specific columns in the second device section.  In the examples above
the substitution ${3} refers to the third column which is the name of the PDU.

This is handy enough but it would be nicer if we could refer to the third column using
a notation of ${PDU} making things nice and clear.  Well you can.  Look at this:

```
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
%%
SERIAL     MAC               PDU  IPADDRESS    SUBNET
PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
PK60860023,00:0d:5d:07:6a:85,pdu4,192.168.8.23,24
PK60867390,00:0d:5d:7b:8f:9c,pdu5,192.168.8.24,24
PK60867769,00:0d:5d:23:91:7a,pdu6,192.168.8.25,24
PK60861021,00:0d:5d:89:3a:37,pdu7,192.168.8.26,24
PK60863094,00:0d:5d:03:4c:1b,pdu8,192.168.8.27,24
PK60863926,00:0d:5d:8e:44:2e,pdu9,192.168.8.28,24
PK60867901,00:0d:5d:aa:b7:07,pdu10,192.168.8.29,24
%%
pdu.name=${PDU}
net.interfaces[eth0].ipv4.enabled=1
net.interfaces[eth0].ipv4.config_method=static
net.interfaces[eth0].ipv4.static.addr_cidr.addr=${IPADDRESS}
net.interfaces[eth0].ipv4.static.addr_cidr.prefix_len=${SUBNET}
net.interfaces[eth0].ipv6.enabled=0
```

Two things have happened here.  There is an extra line:

```
SERIAL     MAC               PDU  IPADDRESS    SUBNET
```

just before the list of devices which assign names to each of the columns.  This then
allows the lines in the third config section to use those names like ${IPADDRESS} instead
of numbers like ${4} which helps reduce mistakes.

This also has the advantage that if new columns are introduced or the order of
existing columns is changed there is no need to change the numbers in the config section.

## New @@ macros

While it is obvious what a line like:

```
pdu.name=${3}
```

means it might not be so obvious what:

```
net.interfaces[eth0].ipv4.static.addr_cidr.prefix_len=${5}
```

means.

To make things easier there is the @@ macro.  Look at the following third config section:

```
@@PDUNAME@@=${PDU}
@@IPv4ENABLED@@=1
@@IPv4CONFIG@@=static
@@IPv4ADDRESS@@=${IPADDRESS}
@@IPv4SUBNET@@=${SUBNET}
@@IPv6ENABLED@@=0
```

If the name between the first @@ and the second @@ is recognised as a built in macro
the `massdeploy.py` utility will change it to the appropriate test.

## Summary

So now we have a `massdeploy.txt` which looks like:

```
#
# massdeploy.txt
#
# version 007 - 16-september-2019
#
# PDUs in data hall 7, first floor
#
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
%%
SERIAL     MAC               PDU  IPADDRESS    SUBNET
PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
PK60860023,00:0d:5d:07:6a:85,pdu4,192.168.8.23,24
PK60867390,00:0d:5d:7b:8f:9c,pdu5,192.168.8.24,24
PK60867769,00:0d:5d:23:91:7a,pdu6,192.168.8.25,24
PK60861021,00:0d:5d:89:3a:37,pdu7,192.168.8.26,24
PK60863094,00:0d:5d:03:4c:1b,pdu8,192.168.8.27,24
PK60863926,00:0d:5d:8e:44:2e,pdu9,192.168.8.28,24
PK60867901,00:0d:5d:aa:b7:07,pdu10,192.168.8.29,24
%%
@@PDUNAME@@=${PDU}
@@IPv4ENABLED@@=1
@@IPv4CONFIG@@=static
@@IPv4ADDRESS@@=${IPADDRESS}
@@IPv4SUBNET@@=${SUBNET}
@@IPv6ENABLED@@=0
```

When this is processed by the `massdeploy.py` utilty it produces
a `fwupdate.cfg` containing:

```
user=admin
password=raritan
log=log.txt
config=config.txt
device_list=devices.csv
```

A `devices.csv` file containing:

```
PK60861100,00:0d:5d:b6:53:6b,pdu1,192.168.8.20,24
PK60860061,00:0d:5d:c7:48:53,pdu2,192.168.8.21,24
PK60867699,00:0d:5d:9e:c0:45,pdu3,192.168.8.22,24
PK60860023,00:0d:5d:07:6a:85,pdu4,192.168.8.23,24
PK60867390,00:0d:5d:7b:8f:9c,pdu5,192.168.8.24,24
PK60867769,00:0d:5d:23:91:7a,pdu6,192.168.8.25,24
PK60861021,00:0d:5d:89:3a:37,pdu7,192.168.8.26,24
PK60863094,00:0d:5d:03:4c:1b,pdu8,192.168.8.27,24
PK60863926,00:0d:5d:8e:44:2e,pdu9,192.168.8.28,24
PK60867901,00:0d:5d:aa:b7:07,pdu10,192.168.8.29,24
```

A `config.txt` file containing:

```
pdu.name=${3}
net.interfaces[eth0].ipv4.enabled=1
net.interfaces[eth0].ipv4.config_method=static
net.interfaces[eth0].ipv4.static.addr_cidr.addr=${4}
net.interfaces[eth0].ipv4.static.addr_cidr.prefix_len=${5}
net.interfaces[eth0].ipv6.enabled=0
```

## Built in macros

Near the top of the Python code in the `massdeploy.py` utility are lines similar to:

```
macros = {
         'PDUNAME':        'pdu.name',
         'IPv4ENABLED':    'net.interfaces[eth0].ipv4.enabled',
         'IPv4CONFIG':     'net.interfaces[eth0].ipv4.config_method',
         'IPv4ADDRESS':    'net.interfaces[eth0].ipv4.static.addr_cidr.addr',
         'IPv4SUBNET':     'net.interfaces[eth0].ipv4.static.addr_cidr.prefix_len',
         'IPv4GATEWAY':    'net.routing.ipv4.default_gateway_addr',
         'IPv6ENABLED':    'net.interfaces[eth0].ipv6.enabled',
         'DNS1':           'net.dns.server_addrs._e_.0',
         'DNS2':           'net.dns.server_addrs._e_.1',
         'DNS3':           'net.dns.server_addrs._e_.2',
         'BLOCKTIMEOUT':   'security.block_time',
         'FAILEDLOGINS':   'security.max_login_fails',
         }
```

To add new macros just insert new lines conforming to the existing syntax.

## Benefits

Here are the key benefits of the `massdeploy.py` utility:

* No need for Excel.
* Works on Windows and Linux.
* Comment feature handy to document mass deployments and comment out lines while debugging.
* Ability to refer to columns by name instead of column number which avoids renumbering issues.
* Use of @@ macros can keep things plain and simple

## To Do List

Think of a clean way to add new @@ built in macros.

If no user= or password= line in the first section either report an error or
set defaults of user=admin and password=raritan respectively.

-------------------------------

End of README.md
