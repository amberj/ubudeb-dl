#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ''
