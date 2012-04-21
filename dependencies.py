#! /usr/bin/env python
# -*- coding: utf-8 -*-
import netfunc
import stripstr

def resolve(url, depends, recommends, suggests):
    print '\nDownloading (and creating) list of dependecies. Please wait...'
    tocrawlh = [url]     # tocrawl history
    tocrawl = [url]
    crawled = []
    while tocrawl:
        popped = tocrawl.pop()
        page = netfunc.get_page(popped)
        if popped not in crawled:
            crawled.append(popped)
            #print crawled
            #print page[:300]
            if page != '':
                temp = page.find('<ul class="uldep">')
                dep_snum = page.find('<ul class="uldep">', temp + len('<ul class="uldep">'))
                dep_enum = page[dep_snum:].find('</ul>')
                part_dep = page[dep_snum:dep_snum + dep_enum]
    
                temp = page.find('<ul class="ulrec">')
                rec_snum = page.find('<ul class="ulrec">', temp + len('<ul class="ulrec">'))
                rec_enum = page[rec_snum:].find('</ul>')
                part_rec = page[rec_snum:rec_snum + rec_enum]
    
                temp = page.find('<ul class="ulsug">')
                sug_snum = page.find('<ul class="ulsug">', temp + len('<ul class="ulsug">'))
                sug_enum = page[sug_snum:].find('</ul>')
                part_sug = page[sug_snum:sug_snum + sug_enum]
            else:
                print 'Error: Could not connect to http://packages.ubuntu.com/'
                print 'Script will exit now...'
                return -1
    
    ###############################################################################
    ######################### TODO: suggests and recommends ######################
    ################################################################################
    
    
    #tocrawl = []
        if depends == 1:
        #l = len(part_dep)
            #print part_dep
            while len(part_dep) > 20:
        #tocrawl = []    
                start = part_dep.find('<dl>')
                end = part_dep.find('</dl>')
                part = part_dep[start:end]
                pos1 = part.find('<a href="')
            #print pos1
                pos2 = part.find('">',pos1)
            #print pos2
                if 'http://packages.ubuntu.com' + part[pos1 + len('<a href="'): pos2] not in tocrawlh:
                    tocrawlh.append('http://packages.ubuntu.com' + part[pos1 + len('<a href="'): pos2])
                    tocrawl.append('http://packages.ubuntu.com' + part[pos1 + len('<a href="'): pos2])
                #print tocrawl[-1]
                part_dep = part_dep[end+ len('</dl>'):]
            #print tocrawl
            #raw_input()
        #print tocrawl
    return crawled
    #if recommends == 1:
    #if suggests == 1:
    #print part_dep

def gen_download_url(url, flag):
    dl_urls = []
    dl_urls_temp = []
    page = netfunc.get_page(url)
    
    pat1 = '<div id="pdownload">'
    pat2 = '</div> <!-- end pdownload -->'
    part_of_page = stripstr.part_of_str(page, pat1, pat2)
    
    if flag == 'sourcenames':
        pat1 = '<td><a href="'
        pat2 = '">'
        len_pat1 = len(pat1)
        
        loc1 = part_of_page.find(pat1)
        while loc1 != -1:
            loc2 = part_of_page[loc1:].find(pat2)
            dl_urls.append(part_of_page[loc1 + len_pat1:loc1 + loc2])
            
            part_of_page = part_of_page[loc1 + loc2:]
            loc1 = part_of_page.find(pat1)
        
        return dl_urls
    
    else:
        #print '#####################'
        pat1 = '<th><a href="'
        pat2 = '">'
        len_pat1 = len(pat1)
        
        loc1 = part_of_page.find(pat1)
        start_of_url = 'http://packages.ubuntu.com'
        while loc1 != -1:
            loc2 = part_of_page[loc1:].find(pat2)
            dl_urls_temp.append(start_of_url + part_of_page[loc1 + len_pat1:loc1 + loc2])
            part_of_page = part_of_page[loc1 + loc2:]
            loc1 = part_of_page.find(pat1)
        
        flag_slash = '/' + flag + '/'
        for item in dl_urls_temp:
            if item.find(flag_slash) != -1:
                dl_urls.append(choose_url_mirror(item))
                #print '**********'
                return dl_urls
        
        for item in dl_urls_temp:
            all_loc = item.find('/all/')
            if all_loc != -1:
                dl_urls.append(choose_url_mirror(item))
                #print '$$$$$$$$$$$$'
                return dl_urls
    
    return 1
        ###########'TODO'
        ### DELETE THIS

def choose_url_mirror(url):
    page = netfunc.get_page(url)
    
    pat1 = '<p>You can download the requested file from the '
    pat2 = '<div id="pdownloadnotes">'
    part_of_page = stripstr.part_of_str(page, pat1, pat2)
    
    pat3 = '<li><a href="'
    pat4 = '">'
    loc3 = part_of_page.find(pat3)
    loc4 = part_of_page[loc3:].find(pat4)
    
    return part_of_page[loc3 + len(pat3): loc3 + loc4]
