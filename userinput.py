#! /usr/bin/env python
# -*- coding: utf-8 -*-
import netfunc

def release():
    page = netfunc.get_page('http://packages.ubuntu.com/')
    #print page
    if page != '':
        # Find locations of part of file that interests us
        # And then, strip that part in another string 'part_page'
        search_start = '<h2>Browse through the lists of packages:</h2>'
        temp1 = page.find(search_start)
        search_end = '</ul>'
        temp2 = page[temp1:].find(search_end)
        # Final start and end locations of part of page which interest us
        start_loc = temp1 + len(search_start)
        end_loc = temp1 + temp2 + len(search_end)
        # Let's slice part of page (which interests us) now
        part_page = page[start_loc:end_loc]
    else:
        print 'Error: Could not connect to http://packages.ubuntu.com/'
        print 'Script will exit now...'
        return -1
    
    # List of releases
    releases = []
    
    # start pattern and end pattern
    spat = '<li><a href="'
    epat = '/">'
    len_spat = len(spat)
    while len(part_page) > 50:
        sloc = part_page.find(spat)
        eloc = part_page.find(epat)
        releases.append(part_page[sloc + len_spat:eloc])
        part_page = part_page[eloc + len(epat):]
    
    releases.append('all')
    
    print '\nList of available releases:'
    i = 0
    j = len(releases)
    for item in releases:
        print '  [', str(i).rjust(2), '] or [', str(-j).rjust(3), ']', item
        i += 1
        j -= 1
    try:
        rnum = input('Enter release number = ')
        return releases[rnum]
    except:
        print 'Invalid release number input!'
        print 'Program will exit now...'
        return -1

def searchon():
    searchl = ['Package names only', 'Descriptions', 'Source  package names']
    print '\nSearch on:'
    i = 0
    j = len(searchl)
    for item in searchl:
        print '  [', str(i).rjust(2), '] or [', str(-j).rjust(3), ']', item
        i += 1
        j -= 1
    try:
        snum = input('Enter option number to search:')
        if snum == 0 or snum == -3:
            return 'names'
        elif snum == 1 or snum == -2:
            return 'all'
        elif snum == 2 or snum == -1:
            return 'sourcenames'
        else:
            print 'Invalid "Search on" option number!'
            print 'Program will exit now...'
            return -1
        #return searchl[snum]
    except:
        print 'Invalid "Search on" option number!'
        print 'Program will exit now...'
        return -1

def sections():
    seclist = ['main', 'multiverse', 'restriced', 'universe', 'all']
    print 'Section:'
    i = 0
    j = len(seclist)
    for item in seclist:
        print '  [', str(i).rjust(2), '] or [', str(-j).rjust(3), ']', item
        i += 1
        j -= 1
    try:
        secnum = input('Enter Section number to search:')
        return seclist[secnum]
    except:
        print 'Invalid "Section" option number!'
        print 'Program will exit now...'
        return -1

def exact_func():
    exact = raw_input('Only show exact matches [y] or [n]:')
    if exact == 'y' or exact == 'Y':
        return 1
    elif exact == 'n' or exact == 'N':
        return 0
    else:
        print 'Invalid input! Only [Y]es or [N]o are allowed'
        print 'Program will exit now...'
        return -1

def architecture():
    archlist = ['i386', 'amd64']
    print 'Architecture:'
    i = 0
    j = len(archlist)
    for item in archlist:
        print '  [', str(i).rjust(2), '] or [', str(-j).rjust(3), ']', item
        i += 1
        j -= 1
    try:
        archnum = input('Enter Architecture number to search:')
        return archlist[archnum]
    except:
        print 'Invalid "Architecture" option number!'
        print 'Program will exit now...'
        return -1

def uinput():

    keyword = raw_input('Enter keyword to search = ')
    if keyword == '':
        print 'keyword not valid or missing'
        print ' Program willexit now...'
        return -1, []
    
    search_on = searchon()
    if search_on == -1:
        return -1, []
    
    suite = release()
    if suite == -1:
        return -1, []
    
    exact = exact_func()
    if exact == -1:
        return -1, []
    
    
    
    section = sections()
    if section == -1:
        return -1, []
    arch = architecture()
    if arch == -1:
        return -1, []
    #print keyword, suite, search_on, exact, section, arch
    
    options = [keyword, search_on, exact, suite, section, arch]
    return 0, options
