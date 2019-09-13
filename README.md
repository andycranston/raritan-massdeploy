# raritan-massdeploy

Utility to create the necessary files for a Raritan mass deployment via USB keys or DHCP+TFTP



# massdeploy.py - utility to create Raritan mass deployment files

## Benefits

No need for Excel
Works on Windows and Linux
Comment feature handy for debugging
Create config files n actual TFTP directory as Excel not likely to be available on the TFTP server itself
Ability to refer to columns by name instead of column number which avoids renumbering issues


-----------

command line params

set directive char/string to ...

new features

config directives:
    @PDUNAME=${PDUNAME}
    @DNS1=${DNS1}
    @GATEWAY=${GATEWAY}

get directives from massdeploy.cfg making it extensible

if no user or password or config or device_List specified add automatically with defaults





-----------

End of README.md
