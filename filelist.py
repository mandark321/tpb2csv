#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 andronikov
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

import requests
import lxml.html
from lxml.html.soupparser import fromstring

import csv

empty_filelist = u'<div style="background:#FFFFFF none repeat scroll 0%clear:left;margin:0;min-height:0px;padding:0;width:100%;">\n<table style="border:0pt none;width:100%;font-family:verdana,Arial,Helvetica,sans-serif;font-size:11px;">\n</table>\n</div>\n'

def get_filelist(torrent_id, protocol):
    print "Getting filelist:",
    r = requests.get(protocol + "://thepiratebay.sx/ajax_details_filelist.php?id=" + str(torrent_id), headers={'user-agent': 'Archiving The Pirate Bay!'})
    if (r.status_code == 200):
        if (unicode(r.content.decode('ISO-8859-1')) == empty_filelist):
            print str(r.status_code) + ", but no filelist"
            return 0
        print r.status_code

        first_level = str(int(torrent_id) / 1000000) + "xxxxxx/"
        second_level = str(int(torrent_id) / 100000) + "xxxxx/"
        third_level = str(int(torrent_id) / 10000) + "xxxx/"

        if not os.path.exists("data/"):
            os.makedirs("data/")
        if not os.path.exists("data/" + first_level):
            os.makedirs("data/" + first_level)
        if not os.path.exists("data/" + first_level + second_level):
            os.makedirs("data/" + first_level + second_level)
        if not os.path.exists("data/" + first_level + second_level + third_level):
            os.makedirs("data/" + first_level + second_level + third_level)
        if not os.path.exists("data/" + first_level + second_level + third_level + str(torrent_id)):
            os.makedirs("data/" + first_level + second_level + third_level + str(torrent_id))

        path = "data/" + first_level + second_level + third_level + str(torrent_id)

        filelist_csv = open(path + "/filelist.csv", 'w')
        filelist_csv.write(u'\ufeff'.encode('utf-8')) # BOM
        csv_writer = csv.writer(filelist_csv)
        csv_writer.writerow(['Filename','Size','Unit'])
        html = fromstring(unicode(r.content, 'utf-8').replace('</td><td align="right">',u'\xa0'))
        filetable = [fileentry.split(u'\xa0') for fileentry in html.xpath('div/table')[0].text_content().split('\n')[1:-1]]
        for entry in filetable:
            entry[-1] = entry[-1][0]
        for entry in filetable:
            csv_writer.writerow([column.encode('utf-8') for column in entry])
    else:
        print r.status_code

if __name__ == '__main__':
	get_filelist(sys.argv[1], 'http')
