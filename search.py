#! /usr/bin/env python
# -*- coding: utf-8 -*-
import netfunc
import stripstr

def results(url, sflag):
    info = ''
    page = netfunc.get_page(url)
    part_page = stripstr.part_of_str(page, '<div id="psearchres">', '</div>')
    
    pac_list = []
    
    pattern1_1 = '<h3>Package '
    pattern1_2 = '<h3>Source Package '
    if sflag == 'sourcenames':
        pattern1 = pattern1_2
    else:
        pattern1 = pattern1_1
    i = 0
    while True:
        #print "#"
        pac_name = stripstr.part_of_str(part_page, pattern1, '</h3>')
        if pac_name == 1:
            break
        
        pat1 = '<a class="resultlink" href="'
        loc1 = part_page.find(pat1)
        
        pat2 = '">'
        pat3_1 = '[<strong class="'
        pat3_2 = '<br>'
        if part_page[loc1:].find(pat3_1) < part_page[loc1:].find(pat3_2):
            pat3 = pat3_1
        else:
            pat3 = pat3_2
        tempstr = stripstr.part_of_str(part_page[loc1:], pat2, pat3)
        #print tempstr
        pat4 = '</a>'
        loc4 = tempstr.find(pat4)
        # Find [category, description] of package in a list
        if sflag == 'sourcenames':
            cat_desc = tempstr[loc4 + len(pat4):].rsplit(': ')
        else:
            cat_desc = tempstr[loc4 + len(pat4):].rsplit('\n')
        #print cat_desc
        pac_category, pac_desc  = cat_desc[0], cat_desc[1]
        pac_desc = pac_desc.strip()
        
        info = pac_name + ': [' + tempstr[:loc4] + ']' + pac_category + ' ' + pac_desc
        print str(i) + '. ' + info.rstrip('\n')
        
        part_url = tempstr[:loc4] + '/' + pac_name
        pac_list.append(part_url)
        #print part_url
        
        loc3 = part_page[loc1:].find(pat3)
        part_page = part_page[loc1 + loc3:] 
        
        i += 1
    
    selected = input('Enter the package number to download = ')
    if selected < len(pac_list) and selected >= 0:
        #print '#######'
        #print pac_list[selected]
        return pac_list[selected]
    else:
        print 'Invalid input!'
        print 'Program will exit now...'
        return 1

