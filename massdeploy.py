#! /usr/bin/python3
#
# @(!--#) @(#) massdeploy.py, version 006, 12-september-2019
#
# from a file called massdeploy.txt generate the Raritan
# mass deployment files
#
# Links:
#
#    The extra config lines for ISC DHCP server configuration file
#    https://help.raritan.com/px2-2000/v3.5.0/en/#41805.htm
#
#    Good blog post by Henry Hsu
#    https://www.raritan.com/blog/detail/how-to-rapidly-configure-intelligent-rack-pdus
#

#################################################################

import sys
import os
import argparse

#################################################################

DEFAULT_MASSDEPLOY_FILENAME   = 'massdeploy.txt'
DEFAULT_SECTION_DELIMITER     = '%%'
DEFAULT_COMMENT_STRING        = '#'

FWUPDATE_FILENAME   = 'fwupdate.cfg'
CONFIG_FILENAME     = 'config.txt'
DEVICES_FILENAME    = 'devices.csv'


#################################################################

def copyfile(sourcefilename, destfilename):
    try:
        sourcefile = open(sourcefilename, 'r', encoding='utf-8')
    except IOError:
        return False

    try:
        destfile = open(destfilename, 'w', encoding='utf-8')
    except IOError:
        sourcefile.close()
        return False

    for line in sourcefile:
        print(line, end='', file=destfile)

    destfile.close()
    sourcefile.close()

    return True

#################################################################

def backupfile(filename):
    if not os.path.exists(filename):
        return True

    index = 0

    while True:
        backupfilename = '{}.{:03d}'.format(filename, index)

        if not os.path.exists(backupfilename):
            break
        else:
            index += 1

            if index > 999:
                return False
    
    return copyfile(filename, backupfilename)

#################################################################

def isnamesline(line):
    for c in line:
        if c.isupper() or c.islower() or c.isdigit() or (c == ' ') or (c == '-'):
            pass
        else:
            return False

    return True

#################################################################

def tokenreplace(line, tokenlist):
    replaceline = ''

    while True:
        openindex = line.find('${')

        if openindex == -1:
            replaceline += line
            return True, replaceline

        closeindex = line.find('}')

        if closeindex == -1:
            return False, 'No closing brace'

        if closeindex < openindex:
            return False, 'Closing brace before opening brace'

        if (closeindex - openindex) == 2:
            return False, 'Opening and closing braces right next to each other'

        token = line[openindex+2:closeindex]

        if token.isdigit():
            pass
        else:
            try:
                columnindex = tokenlist.index(token)
            except ValueError:
                return False, 'Cannot find column name "{}"'.format(token)
            token = '{}'.format(columnindex+1)

        replaceline += line[:openindex+2]
        replaceline += token
        replaceline += '}'

        line = line[closeindex+1:]

#################################################################

def processmassdeployfile(massdeployfile, fwupdatefile, configfile, devicesfile, sectiondelimiter, commentstring):
    global progname

    lencommentstring = len(commentstring)

    linenum = 0
    section = 1
    columnnames = []

    for line in massdeployfile:
        linenum += 1

        line = line.rstrip()

        if lencommentstring > 0:
            if len(line) >= lencommentstring:
                if line[:lencommentstring] == commentstring:
                    continue

        if line == sectiondelimiter:
            section += 1

            if section > 3:
                print('{}: too many section delimiters "{}" in mass deploy file'.format(progname, sectiondelimiter))
                sys.exit(1)

            continue

        if section == 1:
            print(line, file=fwupdatefile)
        elif section == 2:
            if (len(columnnames) == 0) and isnamesline(line):
                columnnames = line.split()
            else:
                print(line, file=devicesfile)
        elif section == 3:
            success, trline = tokenreplace(line, columnnames)
            if success:
                print(trline, file=configfile)
            else:
                print('{}: token replace error at line {} - {}'.format(progname, linenum, trline), file=sys.stderr)
                sys.exit(1)
        else:
            print('{}: logic error - unrecognised section number {}'.format(progname, section), file=sys.stderr)
            sys.exit(1)

    if section != 3:
        print('{}: not enough section delimiters "{}" in mass deploy file'.format(progname, sectiondelimiter))
        sys.exit(1)

    return

#################################################################

#
# Main
#

def main():
    global progname

    parser = argparse.ArgumentParser()
        
    parser.add_argument('--file',     help='massdeploy config file',      default=DEFAULT_MASSDEPLOY_FILENAME)
    parser.add_argument('--section',  help='section delimiter string',    default=DEFAULT_SECTION_DELIMITER)
    parser.add_argument('--comment',  help='comment string',              default=DEFAULT_COMMENT_STRING)
    parser.add_argument('--disable',  help='disable comment processing',  action="store_true")

    args = parser.parse_args()
    
    massdeployfilename = args.file
    sectiondelimiter   = args.section
    commentstring      = args.comment

    if args.disable:
        commentstring = ''

    try:
        massdeployfile = open(massdeployfilename, 'r', encoding='utf-8')
    except IOError:
        print('{}: unable to open mass deployment file "{}" for reading'.format(progname, massdeployfilename), file=sys.stderr)
        sys.exit(1)

    if backupfile(FWUPDATE_FILENAME) == False:
        print('{}: unable to backup fwupdate file "{}"'.format(progname, FWUPDATE_FILENAME), file=sys.stderr)
        sys.exit(1)

    try:
        fwupdatefile = open(FWUPDATE_FILENAME, 'w', encoding='utf-8')
    except IOError:
        print('{}: unable to open fwupdate file "{}" for writing'.format(progname, FWUPDATE_FILENAME), file=sys.stderr)
        sys.exit(1)

    if backupfile(CONFIG_FILENAME) == False:
        print('{}: unable to backup config file "{}"'.format(progname, CONFIG_FILENAME), file=sys.stderr)
        sys.exit(1)

    try:
        configfile = open(CONFIG_FILENAME, 'w', encoding='utf-8')
    except IOError:
        print('{}: unable to open config file "{}" for writing'.format(progname, CONFIG_FILENAME), file=sys.stderr)
        sys.exit(1)

    if backupfile(DEVICES_FILENAME) == False:
        print('{}: unable to backup devices file "{}"'.format(progname, DEVICES_FILENAME), file=sys.stderr)
        sys.exit(1)

    try:
        devicesfile = open(DEVICES_FILENAME, 'w', encoding='utf-8')
    except IOError:
        print('{}: unable to open devices file "{}" for writing'.format(progname, DEVICES_FILENAME), file=sys.stderr)
        sys.exit(1)

    processmassdeployfile(massdeployfile, fwupdatefile, configfile, devicesfile, sectiondelimiter, commentstring)

    massdeployfile.close()
    fwupdatefile.close()
    configfile.close()
    devicesfile.close()

    return 0

#################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
