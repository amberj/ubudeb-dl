#! /usr/bin/env python
# -*- coding: utf-8 -*-
import userinput
#import netfunc
#import stripstr
import dependencies
import search


def upd():
    print 'Ubuntu Package Downloader v0.1\n'
    
    #options = []
    
    # Input options from user
    status, options = userinput.uinput()
    if status == -1:
        return 1        # ERROR
    #print options
    
    # Generate search url from 'options' which looks like:
    # options = [keyword, search_on, exact, suite, section, arch]
    search_url = 'http://packages.ubuntu.com/search?' + 'keywords=' + options[0] + '&searchon=' + options[1] + '&exact=' + str(options[2]) + '&suite=' + options[3] + '&section=' + options[4] + '&arch=' + options[5]
    
    part_of_url = search.results(search_url, options[1])
    if part_of_url == 1:
        return 1        # ERROR
    
    if options[1] == 'sourcenames':
        selected_url = 'http://packages.ubuntu.com/source/' + part_of_url
    else:
        selected_url = 'http://packages.ubuntu.com/' + part_of_url
    
    #### FIX ARGUMENTS depends, recommends, suggests for resolve()
    dependencies_urls = dependencies.resolve(selected_url, 1, 1, 1)
    download_urls = []
    #print '########', dependencies_urls
    for item in dependencies_urls:
        if options[1] == 'sourcenames':
            # Pass 'sourcenames' as second argument to function
            dl_url_list = dependencies.gen_download_url(selected_url, options[1])
        else:
            # Pass architecture (i386/amd64) as second argument to function
            dl_url_list = dependencies.gen_download_url(selected_url, options[5])
        
        if dl_url_list == 1:
            print 'Something bad happened! This should not have happened.'
            print 'BUG #1: Please report this to developers. Thanks.\n Program will exit now...'
            return 1        # ERROR
        else:
            for eachurl in dl_url_list:
                download_urls.append(eachurl)
    
    
    # Generate package download script
    f = open('script.sh', 'w')
    f.write('#!/bin/sh\n')

    for everyurl in download_urls:
        f.write('wget -c ' + everyurl + '\n')

    f.close()


upd()
#dependencies.resolve('http://packages.ubuntu.com/oneiric/smc', 1, 1, 1)
