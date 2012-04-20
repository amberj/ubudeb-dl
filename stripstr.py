#! /usr/bin/env python
# -*- coding: utf-8 -*-

def part_of_str(inputstr, start_pat, end_pat):
    start_loc = inputstr.find(start_pat)
    if start_loc == -1:
        return 1
    
    end_loc = inputstr[start_loc:].find(end_pat)
    if end_loc == -1:
        return 1
    
    return inputstr[start_loc + len(start_pat): start_loc + end_loc]

###########################
######What if start or end or both pat dont exist in inputstr
##### Add error handling
##########################
