#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import csv
from datetime import datetime
import sys

types = {
    '100': 'Audio',
    '101': 'Audio > Music',
    '102': 'Audio > Audio books',
    '103': 'Audio > Sound clips',
    '104': 'Audio > FLAC',
    '199': 'Audio > Other',
    '200': 'Video',
    '201': 'Video > Movies',
    '202': 'Video > Movies DVDR',
    '203': 'Video > Music videos',
    '204': 'Video > Movie clips',
    '205': 'Video > TV shows',
    '206': 'Video > Handheld',
    '207': 'Video > Highres - Movies',
    '208': 'Video > Highres - TV shows',
    '209': 'Video > 3D',
    '299': 'Video > Other',
    '300': 'Applications',
    '301': 'Applications > Windows',
    '302': 'Applications > Mac',
    '303': 'Applications > UNIX',
    '304': 'Applications > Handheld',
    '305': 'Applications > IOS (iPad/iPhone)',
    '306': 'Applications > Android',
    '399': 'Applications > Other OS',
    '400': 'Games',
    '401': 'Games > PC',
    '402': 'Games > Mac',
    '403': 'Games > PSx',
    '404': 'Games > XBOX360',
    '405': 'Games > Wii',
    '406': 'Games > Handheld',
    '407': 'Games > IOS (iPad/iPhone)',
    '408': 'Games > Android',
    '499': 'Games > Other',
    '500': 'Porn',
    '501': 'Porn > Movies',
    '502': 'Porn > Movies DVDR',
    '503': 'Porn > Pictures',
    '504': 'Porn > Games',
    '505': 'Porn > HighRes - Movies',
    '506': 'Porn > Movie clips',
    '599': 'Porn > Other',
    '600': 'Other',
    '601': 'Other > E-books',
    '602': 'Other > Comics',
    '603': 'Other > Pictures',
    '604': 'Other > Covers',
    '605': 'Other > Physibles',
    '699': 'Other > Other'
    }

icons = {
    '[A]': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAALAgMAAAARsAUkAAAADFBMVEW9u7b////a2NIvLSftlLkiAAAAAWJLR0QCZgt8ZAAAAAlwSFlzAAAASAAAAEgARslrPgAAADhJREFUCNdjYIAC0VAQCGGQWgUCSxikfv3btXvXEwbpda/3/d4HpP+93r17N5gPFYfIw9TD9EMBAF1GJTMvV0QlAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDEyLTA1LTI5VDE3OjE2OjQzLTA1OjAwGy3KDQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxMi0wNS0yOVQxNzoxNjo0My0wNTowMGpwcrEAAAAASUVORK5CYII=" alt="Admin" title="Admin" style="width:11px;" border=\'0\' />',
    '[H]': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAALCAYAAACprHcmAAAAV0lEQVQYlZWQUQ7AMAhCodn9r8x+hrNGu4yfVvuCFkqCReItHkmg7+sE1v7KD9mlqzfYLobqtA3+Wilgu00nABBQjJ7ScD/g7kN1Jf7J+crQyVkC2zQm3dAxMgmXoHJyAAAAAElFTkSuQmCC" alt="Helper" title="Helper" style="width:11px;" border=\'0\' />',
    '[M]': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAALAgMAAAARsAUkAAAADFBMVEW9u7b////a2NIvLSftlLkiAAAAAWJLR0QB/wIt3gAAAAlwSFlzAAAASAAAAEgARslrPgAAAC9JREFUCNdjYIAC0VAQCGGQWgUCSxikVr9f//oXiN69a/c6ZHo1jIbIQ9XD9EMBAOn5Ip7eZl6iAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDEyLTA1LTI5VDE3OjI0OjA5LTA1OjAwpgAthQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxMi0wNS0yOVQxNzoyNDowOS0wNTowMNddlTkAAAAASUVORK5CYII=" alt="Moderator" title="Moderator" style="width:11px;" border=\'0\' />',
    '[S]': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAALCAIAAADjvHrgAAAAf0lEQVQokWPcu3sbA7UBCwMDg5OLJxVN3LdnOwuEdfvmZaqYqKquywBxKRY5DT0GBobbNy7BGXBBXFxkwITLToiJcA0QNgQhG4fMJWwoJQCfoZj+IhJgD1OsFmAGInKIEzYUWR2cjaYZjz+ghkKSArUACwMDw74926loIgMDAwCwij+pKx0wBwAAAABJRU5ErkJggg==" alt="Supermod" title="Supermod" style="width:11px;" border=\'0\' />',
    '[T]': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAALCAYAAACprHcmAAAAVElEQVQYlYWQQRIAIAgCsfH/X6ZLljhZXFJbsTSS2DKkZImwCMcTLPUhF8nlliscLgGVaQp/nnTgcOtOAN6Ozu4rdinUD5YmF+CzZxfo5UzYfRuNJhRKIBtAE2X7AAAAAElFTkSuQmCC" alt="Trusted" title="Trusted" style="width:11px;" border=\'0\' />',
    '[V]': '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAALAQMAAACTYuVlAAAABlBMVEX8//wE7AQzTN4bAAAAAXRSTlMAQObYZgAAAAFiS0dEAf8CLd4AAAAJcEhZcwAAAEgAAABIAEbJaz4AAAAkSURBVAjXY5BnYLBvYNBrYLBuADFEGRjuJzA8eMAAFE84AEQAdTgIei8ZmTAAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTItMDUtMjlUMTc6MTU6NDQtMDU6MDA1vU+AAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDEyLTA1LTI5VDE3OjE1OjQ0LTA1OjAwROD3PAAAAABJRU5ErkJggg==" alt="VIP" title="VIP" style="width:11px;" border=\'0\' />',
    '':    ''
    }

torrent_id = sys.argv[1]

first_level = str(int(torrent_id) / 1000000) + "xxxxxx/"
second_level = str(int(torrent_id) / 100000) + "xxxxx/"
third_level = str(int(torrent_id) / 10000) + "xxxx/"

path = "data/" + first_level + second_level + third_level + str(torrent_id)
    
details_csv = csv.reader(open(path + '/details.csv'))
details_csv.next()
details = details_csv.next()

description_text = open(path + '/description.txt').read()

try:
	filelist_file = open(path + '/filelist.csv')
	filelist_csv = csv.reader(filelist_file)
	filelist_csv.next()

	filelist_rows = []
	for row in filelist_csv:
		filelist_rows.append(row)
	filelist_file_exists = True
except IOError:
	filelist_file_exists = False


try:
	comments_file = open(path + '/comments.csv')
	comments_csv = csv.reader(comments_file)
	comments_csv.next()

	comments_rows = []
	for row in comments_csv:
		comments_rows.append(row)
	comments_file_exists = True
	commentamount = len(comments_rows)
except IOError:
	comments_file_exists = False
	commentamount = 0

title = details[0]
category = details[1]
categorystr = types[category]
files = details[2]
size = details[3]
imdb = details[4]
spoken = details[5]
texted = details[6]
tags = details[7]
qualityplus = details[8]
qualityminus = details[9]
qualitytotal = int(details[8]) + int(details[9])
uploaded = details[10]
by = details[11]
usertype = details[12]
seeders = details[13]
leechers = details[14]
btih = details[15]
dn = title.replace(' ', '+')
picture = details[16]
capturedate = details[17]

uploaded = datetime.strptime(uploaded, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S GMT')
capturedate = datetime.strptime(capturedate, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S GMT')

if spoken == '':
    spoken = 'None'

if texted == '':
    texted = 'None'

if tags == '':
    tags = 'None'
else:
    tags = tags.split(',')

if imdb == '':
    imdb_html = 'None'
else:
    imdb_html = '<a href="$imdb" target="_blank" title="IMDB" rel="nofollow">IMDB</a>'.replace('$imdb', imdb)

tags_html = []
for tag in tags:
    tags_html.append(u'<a href="">' + unicode(tag[1:-1]) + u'</a>')
tags = ' '.join(tags_html)
                     
if qualitytotal >= 0:
    qualitytotal = '+' + str(qualitytotal)
else:
    qualitytotal = '-' + str(qualitytotal)

upper = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<title>$title (download torrent) - TPB</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<style type="text/css">
.searchBox { margin: 6px; width: 300px; vertical-align: middle; padding: 2px; }

.detLink { font-size: 1.2em; font-weight: 400; }

.detDesc { color: rgb(78, 84, 86); }

.detDesc a:hover { color: rgb(0, 0, 153); text-decoration: underline; }

.sortby { text-align: left; float: left; }

.detName { padding-top: 3px; padding-bottom: 2px; }

.viewswitch { font-style: normal; float: right; text-align: right; font-weight: normal; }

body { text-align: center; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 0.7em; margin: 10px; color: rgb(0, 0, 0); background: none repeat scroll 0% 0% rgb(255, 255, 255); line-height: 1.3em; }
a { color: rgb(0, 0, 153); text-decoration: none; border-bottom: 1px dotted rgb(0, 0, 0); }
a:hover { text-decoration: none; border-bottom: 1px solid rgb(0, 0, 153); }
.img, .img:hover { border-bottom: 0px none; }
#searchfield2 { display: block; width: 500px; margin: 0px auto 20px; text-align: center; padding: 0px 0px 0px 10px; }
#TPBlogo { float: left; border: 0px none; padding: 0px 10px 0px 0px; margin-top: -7px; }
h2 { font-size: 1.1em; line-height: 1.5em; text-align: right; padding: 2px 5px; margin: 0px; border-bottom: 1px solid rgb(210, 185, 166); background: none repeat scroll 0% 0% rgb(246, 241, 238); font-weight: normal; clear: both; }
h2 span { font-weight: bold; float: left; font-size: 1.1em; }
.header a { color: rgb(0, 0, 0); }
#searchfield { display: block; width: 650px; height: 200px; margin: 0px auto; text-align: center; vertical-align: bottom; padding: 0px; }
form { vertical-align: bottom; text-align: left; margin: 0px; }
form .inputbox { margin: 6px; width: 300px; vertical-align: middle; padding: 2px; }
.submitbutton { vertical-align: middle; }
.hide { display: none; }


#detailsouterframe { position: relative; margin: 0px auto; width: 680px; text-align: right; padding: 0px; }
#detailsouterframe #delete { text-align: right; padding-right: 4px; width: 20px; background: none repeat scroll 0% 0% rgb(210, 185, 166); float: right; clear: both; font-size: 0.8em; font-weight: bold; }
#delete :hover { border: 1px dashed red; }
#delete a { text-decoration: none; border: 0px none; color: rgb(255, 0, 0); }
#detailsframe { clear: both; border-top: 1px solid rgb(255, 255, 255); background: none repeat scroll 0% 0% rgb(246, 241, 238); text-align: left; overflow: hidden; margin-top: 10px; }
#detailsframe #title { padding: 6px 0px 8px 20px; font-size: 1.2em; text-align: left; font-weight: bold; letter-spacing: 0.07em; border-bottom: 1px solid rgb(255, 255, 255); }
#detailsframe #title { height: 1%; background: none repeat scroll 0% 0% rgb(210, 185, 166); }
#detailsframe #title div { font-weight: bold; float: right; font-size: 0.9em; padding-right: 20px; }
#details { padding: 0px 10px 10px 20px; background: none repeat scroll 0% 0% rgb(246, 241, 238); }
#details h3 { margin: 0px; border-bottom: 1px solid rgb(210, 185, 166); font-size: 1.3em; }
#details h3 em { font-style: normal; text-decoration: underline; }
#details h3 a { text-decoration: none; border-bottom: medium none; }
#details h4 { margin: 20px 0px 0px; color: rgb(123, 86, 58); font-size: 1.2em; }
#details p { margin: 10px 0px 0px 10px; text-align: left; }
#details dl { text-align: left; float: left; margin: 10px 40px 10px 0px; }
#details dt { float: left; font-weight: bold; padding: 0px 5px 0px 0px; color: rgb(123, 86, 58); border-bottom: 1px dashed rgb(232, 220, 210); clear: both; }
#details dd { padding: 0px 0px 0px 40px; border-bottom: 1px dashed rgb(232, 220, 210); }
#details .col1 { width: 307px; }
#details dl.col2 { clear: right; width: 260px; }
#details dl.col2 dd { padding: 0px 0px 0px 70px; }
#details dd img { width: 59px; height: 10px; }
#details #CommentDiv { text-align: left; clear: both; background-color: rgb(246, 241, 238); width: 620px; height: 130px; padding: 10px; margin-top: 10px; margin-bottom: 20px; }
#details #filelist { width: 100%; border: 0px none; }
#filelistContainer { margin: 3em 0px 1em; min-height: 50px; border: 1px solid rgb(210, 185, 166); background: none repeat scroll 0% 0% rgb(255, 255, 255); padding: 10px; clear: left; }
#details pre { white-space: pre-wrap; word-wrap: break-word; font-size: 11px; font-family: "Courier New",Courier,monospace; }
.nfo { margin: 1em 0px; width: 600px; min-height: 50px; border: 1px solid rgb(210, 185, 166); background: none repeat scroll 0% 0% rgb(255, 255, 255); padding: 10px; font-size: 12px; font-family: "Courier New",Courier,monospace; clear: left; line-height: 0.9em; }
p.info { padding: 10px 0px 0px; font-size: 0.9em; clear: both; }
p.info textarea { padding: 3px; font-family: verdana,Arial,Helvetica,sans-serif; font-size: 11px; width: 300px; height: 100px; }
p.info input { margin: 4px 7px 0px 0px; }
.download { clear: both; }
.download a { font-size: 1em; color: rgb(0, 142, 0) ! important; font-weight: bold; text-transform: uppercase; border-bottom: 1px dotted rgb(128, 199, 128); background: url("urn:not-loaded:https://static.thepiratebay.se/img/icons/dl.gif") no-repeat scroll 0px 0px transparent; padding: 0px 0px 0px 13px; }
.download a:hover { color: rgb(0, 142, 0); text-decoration: none; border-bottom: 1px solid rgb(128, 199, 128); }
.detailartist { clear: both; }
.detailartist a { font-size: 1em; color: rgb(0, 142, 0) ! important; font-weight: bold; text-transform: uppercase; border-bottom: 1px dotted rgb(128, 199, 128); background: url("urn:not-loaded:https://static.thepiratebay.se/img/icons/td-nfo.png") no-repeat scroll 0px 0px transparent; padding: 0px 0px 0px 13px; }
.detailartist a:hover { color: rgb(0, 142, 0); text-decoration: none; border-bottom: 1px solid rgb(128, 199, 128); }
#details a.comments { padding: 0px 0px 0px 14px; background: url("urn:not-loaded:https://static.thepiratebay.se/img/icons/comments.gif") no-repeat scroll 0px 3px transparent; }
#details a.list { font-weight: bold; }
table#details { margin: 40px 0px 0px; font-size: 0.9em; width: 100%; border-collapse: collapse; }
th#details, td#details { padding: 1px 4px; border-bottom: 1px solid rgb(255, 255, 255); border-right: 1px solid rgb(255, 255, 255); background: none repeat scroll 0% 0% rgb(246, 241, 238); }
thead#details th#details { background: none repeat scroll 0% 0% rgb(210, 185, 166); }
tbody#details th#details { color: rgb(123, 86, 58); }
.shortcuts { width: 27px; padding: 0px; margin: 0px; }
.shortcuts li { float: left; list-style: none outside none; padding: 0px; margin: 0px; }
.shortcuts a, .shortcuts a:hover { width: 13px; height: 13px; display: block; text-indent: -9999px; padding: 0px; margin: 0px; border: 0px none; background-position: center center; }
.shortcuts .comments a { background: url("urn:not-loaded:https://static.thepiratebay.se/img/icons/comments.gif") no-repeat scroll center center transparent; }
#comments { font-size: 0.9em; }
#comments p { margin: 0.5em 0px 0px 0.5em; padding: 0.3em 0px; }
#comments p.byline { color: rgb(187, 150, 122); margin-top: 12px; }
#comments img { padding-bottom: 0px; vertical-align: bottom; }
#comments .comment { background: none repeat scroll 0% 0% rgb(255, 255, 255); margin-top: 0.3em; }
.browse-coms { text-align: center; margin: 1em 0px; }

#content { position: relative; text-align: left; min-width: 960px; max-width: 1200px; margin: 15px auto 0px; }
#main-content { margin-left: 130px; margin-bottom: 0px; padding-right: 10px; margin-top: 0px; overflow: hidden; position: relative; z-index: 90; }

.torpicture { float: left; width: 280px; margin: 0px 15px 5px 0px; text-align: center; }
.torpicture img { margin: 10px 0px 0px; }

	</style>
</head>

<body>
	<div id="header">
		<form>
			<a href="" class="img"><img src="data:image/gif;base64,R0lGODlhUgBXAPcAAKN5WJuIeZRgO5hmQZxoQ+zr69vSzJlsTKyTgZpoRGlWRreUe5FdOItcO4FUNMGpl7Kci1I0G5NtUls8I5yCbYhrVuTa0rytoptyVfz+/v7+/KKDa8zDu9LKw/Pw64thQpt8ZKiKc+DUyKOMe2ZLNpZzWurj3J1pRHtiT6F9Yq+ai7SilHlNLa2QfM3IwsO1qpVqS0kqEvHs6YRaO+Ld2XxSM+rm4NPDtPv598u9sotZNvX19eXh3bmhjsOypLyrnZZkQdzZ1Z12WPHq41tAK9nMwfP09fj5+fr9/ppnQnxbQsO7sYZdQfb7/IJjSt7c2r2yp4Z0Zp2MgNDFvauNeLuklNXRzpxmQKKIdZ16XvLz8c3Atfj29KWSg5pkPsu7rfX08cy1pHRTOmRAJe7o5IplSpJ8aoRRLmpGKuXk4Vk6H4ZhRI9yXWNCKbGZhv79+9rKvdPIvnJOMvTy725KLZZ5ZNG8rNTX0p1lPm9YSbWlmZdiPZxqRKOGb3JLLI5pT/z+/DgdCKiGbJCDebapnmlDJsChirCVgamDZqydkMGuoJBhP8e3q2A+I5VwVP38/MS5rpdgOLuZgJhnQ/X3+e7x839NKqyYhZVoRZRiQNvX03ZQM3VZQ93Qxfz9/efc07KfkNG/sZBlRHxKJ4VYN4lWNPz7+XpWPJVlQ6R/ZHJXQerg1YJWNkowGkAkD492YqyJb7eeitnQydPMyLqlmN7i45BkQnFFJMXBvI5fPZ5oQZt/aF46Hp5pQ29QOeDXzpljQFY3HYhoTlc2HZBXLqygl/79/bGJbH9bP/////T09HVHKZxjPZ5tSci/uMivmppqR39QL/7+/v7//////v7//v/+/f3+/6aZjJtpRa6LcoFuXol/dOnq6aWViqiWh5tnRO7v79fDtP39/dLQxJxoPT8gCmRHMp5qRJl4X//+/3tdSOPY0JtrSOff2ZBnSVAxGb62s08tFVg1GKF0UsG2rsW+uMfAt29XSGtBIebn5XdFIZ1vT5pkPJthO5V3YCH5BAAAAAAALAAAAABSAFcAAAj/AJMJHEiwoMGDCBMqXMiwocOHECNKnEhwGsWLGCHOOWQho8ePB6eFmAKyZEkfkEyqxEjNjZ6VMCVaqOEmps2F1t5Mi7UPhCmF06pRk0b0Zsk4M6I50aewGqBryYYa/UiGSTQHrKwotEaNzJQMUzFaExjLElYmKaVZHDjt2tghLep5CktxmsUHp86cwQIKQrJqawVamzsk3QUkdOsm6zHqDCsK3YpsOGKQWjIuIRLtSFY0cUQZVs+weUJtVYoCBI1pSAZmA4XNYz1LNEHKQakV1ZLNyaKJmuVkYEVIYLHEYmDZDqf9OlOqAaOo1DY8/82lCitLa54IlIa8Yc7VoaLl/2IAaW2PWAMtIEjqYE2aadwLSnuTTEaB456trZbhqNSeTCQJdAME03jwwAglOEAKK+/wgBBUn4BATne/JUMGBpYswgAITAm0SguhUKDHCA4wsEgmmciiDkKdsEEIDlAZ5QkXGVhGjQbTUBNHGZY0wIAEHSSjgVoeiIJFByOUIgAQA0wiwCFzaXCNBjhS8wMT9YB1jTTWxGYQUfHFF9ERP+xg2TQZ4HCIJdGQwoAjHNRoDXdwkEJOLMRkMskkBFwxCRCGzEHQNW7sM8JPAlGDZkLjbEcRICBolcw0plCxyR+slPKPVkNBBcYl/6QigJ4JJHBCLwQksIcQkoRxQxwtjP/ChFbGdUJDQnbZx9lEYKwBykBkVGFFWSVoJdRfyUBxTwulZDJAAgREywcBeDATiQ4f/OFANJaMQElUAh2yxJdF2bCBVmI+NE0oo9RBmTTXWJQFK7i0taJANFSRQyZ7PAttqn1iAgIES2yRAgMNrEFSfG9gYYBB8FEDBggrIArRWDhgMMoM2lUD1ioOUGCEkDVa9gMEmeQySanZnNAnKhQs0Q01n6QSCTAMjLAZfMl4AEIaBlkTVAvffLvrQ9ao88UoZewChW8CFVGDM2yBxY4EHwjQZBLZTOsFBj/MTE0RfOyRBDDvBChkNSaUoV1BuT1QBtAVQgRIOqMUo8kIOgn/9EkXHqxlDVghnKH1yl1fMcAId8yVTCgneBHtHiMoMxBUncyNXzJ2LPPr5g1RY0Mpa9DwSRk2tGXNNU3cALSQ1MDBCgNA8JlNNkkIAUUlA4WxxxXQnOAnBzkKBNYXJYycqGXsMCEM0HZNVMQoI2TwiwTPITGXO6Dwzh0ZEujgbBIECJ8Fp3aFAQT5J5wwQCqo/TZWFRQgRhAjtY17kTRhsGBPMjaowgYyYJFfgGAK03hLf5wFrfbhIQRNiMojDPG7bBAAGrpAxQUmNZDcHKJ6A6EGBFhgiQAY7SItYEIaqsGOIqQjHMnoRANYEQSLmOAPZxgfH7KhC2hcgR5kmAYX/xYQCXDcjgA8dEQQkuGl3PQBFNN4A3cU0RhkzIKJF6FGCtiwmS+k4RCM8MEIzsCEIFDDFCMgRS4GMIAk8KEXXriCLrIQDg/AIhLRilbLgNGCE05qGkP4gwomlYFQfGBbUsABBymCgz+MIDc+KMAN1rCFVERjBlfkgjtSwYA28hAGEACAPy7BDgDgMY8WJAAq9EeQG1riA7fawi50oAMmuAA6FKmGKSSgh2rg4AU4gIMEeuAjHfwAONPQBgPIR4DFaeET9EgFAPpxglSW7wTgwMCtjpaMG4xiW4rwAQJEwQAGUEALuGRkCag2hzhMIwcYYEAkgCCAVHABOLAQQAKg0f+PdJAmGZIQQD96Yc1reiEE9yyIAa7CCr4cIBKoWAQUPjKHEvRGBgaYgyIQ0ckBeCETcYjKAvRJAEyMyxqhaIYuUmnN9nnBDfYjiDIcYYkS1MOUA9gDBt6WkSJQoBLTcIcB2JGFSbSRfHvYABiS8YwiemEERjCFJH6HxPZZ1apeuED0CgIHB4DiGAJIQhL2gIAIeoQD7kyGBWgQhlKgQqxW3cMzkuEOaOABBi6wRkCZec2ruiwJVNucD3TQDmAkQKyTCKxHjDEOqHTAAMqcBNf40D7gdWIaD2DABoxgCDy6LI9+ddkBZLG5AmyAAf3gWjauIIRaLBIkW6AFKtYH2hP/QONrJjAFIlpgCC+s9HblGEDw/HoFftzqNxqQGC3cENbDRs5bK3kGKRaRhH9dExq9YAYA3HEDLwABidHywgEQwAFEMOOqBDiApAQSL0V0gR/+4Fr5gLHBlbTgDEBIQEtPoIsT8AEYzQAAOHqBqisAYRcuiOBU0XsATUwKajy4BAyWSYAdZgMct0zXRwShg/ym8gR48AIwUHGAZlzhCidAxxX24AhCiC0ZD9jDVVmrD3VUgys4UEQWdPCsaCXgCtpcSTWy0MnbWTABfSDEC6bgAwz0lw+TcMQ37pAjMpiCGnaQsVWvcBqSqeMFJRBfj6OFhy6rZAcS6CQ02jEJDLTj/xAyACAi8FDZdHSgCdPAgTjaUQR1iEBylBVel1cjggboYBFttC4zQkCJunmEGgWAwSKMeIV0tAAd/tBGEUTZvl4AAQLUwIEhQkAFUZBEBvRAcS8EjZr6YEDM7LNqPxDgOJOkYRe1w0M7cCGJSPSiGXw4b8sI4IUliCAOKXiBO2ZxBEVpAxhX8ILwhAC0aiyAGKgYs1WzMetal8QAbgDHFYDxDSR0gh/VvcLt2keAJHAgFS0wAliQBdBcYKEFBNDFAYJgDTswwAuSNZVfvYCAmJbkBj5IgT9gECQLpDq07stBJ0hCDRN0ggePEMcBUCELCwABD5MoAhjoYTZmhhYYCP94BOgw8oI49GBDBQDDMaQN8axexgbU2MIDqAAABggAC3MAgyAGAIQHTFW/fb1qdqlAmYlIYxxdMogirPALBlChCTJoBjggfoI99GAanfCBOKiACmI0AASE2EIRkiEOIGSDHwlYdbQg3gsuh8PRDSlKFL0kEDdowhqICEEGnrEyrntBEJ0whBAYQIwPgEAPG43FAxBBDyRCAxq1DW27m7HNiHDnFx6gBt8f0QV3JOMTG1gAMJLuV13wAxYpoIcQUnGBSthBCH2oxS/8gQc+8OEA7dDF3LmuCy9sgZsQ4cAGyCAkYwjEFG6wgYWEgMdsrBriBMAABA7BAQNUIQyheMb/CnyAg1+AA4m94AMAMLju0BJ4D7GYxpAmwoE6wIEaW2INBLRwA34I4ArDB3GrFQu0sAAA4AWRsAd7gIAL8Az8AID5BgBO5nt0hw4DgAhmkhsRkRsGUAaxgCgeQAhfYDgHkHnuxwyxQETqZmS3I2Is9WsAYH1cNy0E9TATITSn9wfpIH3u8AOycAAwcAAuI3xW5XtGyF/8UHnWNXc8pHQEIAT0oAtGOIUU2AvAsABmpWEPEQ4bwAS/EASEYAEAkAlJQFDNcFVU2D66kAr8IHx59Iasp37NUGFUSIGnsgdfgBH08QigwASpgAGYEAlJ4DL8kAV9lYaEKAR4AIdveCrX/8QH7UAP7eBfddg+fFBcpod3DXENb2AZLWAJDEAqFiQEKaBaLHiKCUAPP0YAk8BA+3RBk4AHh3UFSQANQqBHqMgyeyAIHiAkEoGDcfAHDZAJTLInA0CK/lIqyriMA8APfQANAwACF3AI7ZACI7ABKdACIUAPjtAO63MAKdAO1bWMe7IyTpIKcSYR1GAMbsAC4kOMbER0s9cvRsVGRqWATTIAi0AFPpAFl1ANsiAEIdACVNAHiuB9oCALEIAK/dCN8RiPwAAMEMkAfRBnXKGJCHEBy+AAubAItgAEQECMe3AAIUCMqJAJB3AAQACO6QAD4xEJtpACVHAJWvAE2QgLgv9ABVSQAzngBtqAAaIABJgABJGQC7kAkqKACaKwCONRTmeQAnMQFFTSENNQBCzACkY5KhpyIraACBGFChhwjQIAAz3gDExGBZOgAwyQAnqgBSawAVQQC6lwCAiAAGHQAhKgAofAALawCOkACj8AA7swC5pgBRzgAyczAukwAxJggxrIEDRQA1jZALbwAemAAOHjkZnwAYvAlLmwlA2QC/zQAigRCy7ZB0YwBy2QAi4gCAgAATP5ABsQAiVQTn9gBdyBCH1AQAXhCTVJCxXQAr24cgVhAzPgADrgCGkkCgfZAg3wDkyQCx9QAunwDiUgARjwDgNQCqyACoLgCNiydrT/8A6yUAVU4AYtcAiw8AE6YJQN8A8wNA2CAAJ+ZBAy0AVsYIMNsQtXuQKUUAUNYAkYwAhuoAMNcKAS8AfvsAaU+QEwUAbv8AGkQEukUAZfIEwvQANYgAB9YAsT+gEf4AikQAFG853odBDVkBvT0AE/oEgLwR1WWQMcIBCaAAJmsQG70ACk8A8qMAMfkAukwASVyQQfQKRl8AENwAQ4WgIIkAwIAAOl4AAz8Ae7UAJlcAZdcBlFcABMAArcIXpqUTXJ9QjO96JjAQq3oAhtkQw7AAEOYAlMUAakEKIzwAqsUBv/sAvpUAclYKdlsAYz8AM+MAr/MA1fwAKkIAxYQAF//8AEyEAKiXADMIAVf/AHWCADHuMJjykRRSENbqAEnQAuybAFa/BNrOAANYAVdhoNedoCFdADbFACf8AGDNoDdUAKbuAOEvAKCPAPDaAUa0AKa8ACTtAFZVADyHALFGACHkMfFAEmAsEIFQAK0icQNtAHNZCtqLqtIUMBZpAFbjACXYAFOdAFyLAMa4AM/0ABElABa4CqM+A828AGu4AATMACFfAKr2AGTrACf3Es+zMWBUALFNAFPjAFU2APjrAMNcAC0bAJNWAJSpAIX0ABdQACVYAFa/ANSwABTsACLLAGpzADLLAJyLAGTuAEIBAAwvAHDWsG2KACLkANN+ALD/9DFBiZd5xhGVwgC5BwD1sQB06gBJsAsnJAB05AAZcACrtQAciAAGzwCv9ACFCwAlhwCsVKAeuwBkpQAU6ADDXgB36wCXKwCWYwAmIwUS/gBL6wAoqSsw8BsANRBGJgBmLgB0hLCxegB4lwCYkABZDQBSn7ChdwAZewDsJwCmLwD2wgDBUgDHKwDMvgB0qwDmywDnKAt1+gSMoACedwS3A7ERbxAmgQAMmKtFLwDYlwAVuwBCugAksQBHpAAVOwAXRAtnSABmggBmwgBoVAB3TQtaeABnIgDMiQu6dAAdwBBiSQpSthF4yABlJgBvmABiPAARfwAyvwDQigB84ABSr/0AE+QAe+gAaFcL6FoLuFkA+FIAdDm7vqSwdiIAb50AYjkAgV0Aj1IKof4SU/oAYrEAC8kA/rgAVmEACJUA8c4LrOwAHrMAbmm76qIAYRPAa+oARocA5jcL5tgL5jQAJKQAe8IAW+IAXo5Ggeow5dooW4Uh/fUAGcwAtRQLqNgAZREAA4/LeEkAMjkAe+0Ahj0AZtcLSc4ASFMAbrwK9jsMRtEMRtgAZNzAsW7AsafA8IISZTAhFpsA3yEAyq0AiqQAiqwAu8UAFSEACEkK/YQAKq8MON8MZwPAFtoAq52wYTAMRwPAaN0AZg7ARtMAwQjAacAEz2qQLeYACKEhJu/6EBc6EWj7ANRAAPajAMvBAB22AGEaAGREABUtAFFSAP80AEjaAGE1DKpnzHdHAOE0DKpdwIckwCrswLpYwCdssLw9AGJEAEqoANJjAQgIACEeALwWAGBlcQBMQFAaAdS3AORNAKJOALahAMasAJbaAG87DLZkAC0hzNatDN3vzN2/zNjUAE3lzKahABbcAJKIAP0dwI8BADRBAATIEDRJAH2FAMMUAIPEMQYLgD01APrrANPOACU6AA8pDJwTAMw7DKCj0B5xABERAMEj3RFF3RFK3QFd3NEj0PETABKIACwRABCv3ORIAN4XABRDAIQdAKedB0nMEd2+AK9VAMrdbgCq0QDNvACa0ADxDd0z4dATz900I91ERN1K0QzT3N0zHgCkSwDVEgBShgDufQDWvBHdOQB4HgCoEQCOZgDlttDjEQ1mI91mRd1mZ91mid1mLtCubgCmwdCNzgOEPBHfGgAERABCSgAHqtAHnQ1/jg13/d13nw1/hQ2IYt2Iid2Iq92Iwt2HzN17mM11FwB8ZzI0RxDZQQDvrQDVqwAztgBEagDMoA2kagBaI92lqQ2qo92qEddKT92rAd27Bt2mCgBaANBrWtDFqA20ZQADzAA93g0gEBADs=" id="TPBlogo" alt="The Pirate Bay"></a>
			<b><a href="" title="Search Torrents">Search Torrents</a></b>  | 
			<a href="" title="Browse Torrents">Browse Torrents</a>  | 
			<a href="" title="Recent Torrent">Recent Torrents</a>  | 
			<a href="" title="TV shows">TV shows</a>  | 
			<a href="" title="Music">Music</a>  | 
			<a href="" title="Top 100">Top 100</a>
			<br><input title="Pirate Search" required="" placeholder="Search here..." style="background-color:#ffffe0;" class="searchBox" type="search"><input value="Pirate Search" class="submitbutton" type="submit"><br>
			<label for="audio" title="Audio"><input type="checkbox">Audio</label>
			<label for="video" title="Video"><input type="checkbox">Video</label>
			<label for="apps" title="Applications"><input type="checkbox">Applications</label>
			<label for="games" title="Games"><input type="checkbox">Games</label>
			<label for="porn" title="Porn"><input type="checkbox">Porn</label>
			<label for="other" title="Other"><input type="checkbox">Other</label>

			<select>
        	        	<option selected="selected" value="0">All</option>
				<optgroup label="Audio">
					<option value="101">Music</option>
					<option value="102">Audio books</option>
					<option value="103">Sound clips</option>
					<option value="104">FLAC</option>
					<option value="199">Other</option>
				</optgroup>
				<optgroup label="Video">
					<option value="201">Movies</option>
					<option value="202">Movies DVDR</option>
					<option value="203">Music videos</option>
					<option value="204">Movie clips</option>
					<option value="205">TV shows</option>
					<option value="206">Handheld</option>
					<option value="207">Highres - Movies</option>
					<option value="208">Highres - TV shows</option>
					<option value="209">3D</option>
					<option value="299">Other</option>
				</optgroup>
				<optgroup label="Applications">
					<option value="301">Windows</option>
					<option value="302">Mac</option>
					<option value="303">UNIX</option>
					<option value="304">Handheld</option>
					<option value="305">IOS (iPad/iPhone)</option>
					<option value="306">Android</option>
					<option value="399">Other OS</option>
				</optgroup>
				<optgroup label="Games">
					<option value="401">PC</option>
					<option value="402">Mac</option>
					<option value="403">PSx</option>
					<option value="404">XBOX360</option>
					<option value="405">Wii</option>
					<option value="406">Handheld</option>
					<option value="407">IOS (iPad/iPhone)</option>
					<option value="408">Android</option>
					<option value="499">Other</option>
				</optgroup>
				<optgroup label="Porn">
					<option value="501">Movies</option>
					<option value="502">Movies DVDR</option>
					<option value="503">Pictures</option>
					<option value="504">Games</option>
					<option value="505">HighRes - Movies</option>
					<option value="506">Movie clips</option>
					<option value="599">Other</option>
				</optgroup>
				<optgroup label="Other">
					<option value="601">E-books</option>
					<option value="602">Comics</option>
					<option value="603">Pictures</option>
					<option value="604">Covers</option>
					<option value="605">Physibles</option>
					<option value="699">Other</option>
				</optgroup>
			</select>
		</form>
	</div><!-- // div:header -->

	<h2><span>Details for this torrent</span> </h2>
<div id="content">
<div id="main-content">
<div>
	<div id="detailsouterframe">
	
	<div id="detailsframe">
	<div id="title">
		$title</div>

	<div id="details">
	<dl class="col1">
		<dt>Type:</dt>
		<dd><a href="" title="$type">$typestr</a></dd>

		<dt>Files:</dt>
                <dd><a href="" title="Files" onclick="">$files</a></dd>

		<dt>Size:</dt>
		<dd>$size</dd>
		<br>
			<dt>Info:</dt>
			<dd>$imdb_html</dd>
					<dt>Spoken language(s):</dt>
			<dd>$spoken</dd>
		
					<dt>Texted language(s):</dt>
			<dd>$texted</dd>
		
					<dt>Tag(s):</dt>
			<dd>
			$tags
			</dd>
				<dt>Quality:</dt>
				<dd id="rating" class="">+$qualityplus / -$qualityminus ($qualitytotal)</dd>

		<br>

		<dt>Uploaded:</dt>
		<dd>$uploaded</dd>

		<dt>By:</dt>
		<dd>
		<a href="" title="Browse $by">$by</a> $icontag</dd>
		<br>

		<dt>Seeders:</dt>
		<dd>$seeders</dd>

		<dt>Leechers:</dt>
		<dd>$leechers</dd>

		<dt>Comments</dt>
		<dd><span id="NumComments">$commentamount</span>
				 
				</dd>

		<br>
		<dt>Info Hash:</dt>
		$btih</dl>
<div class="torpicture">
$picturetag
</div>
	<dl class="col2">
	</dl>
		<br>
		<br>
<br><br>	<div class="download">
		<a style="background-image: url(&quot data:image/gif;base64,R0lGODlhDAAMALMPAOXl5ewvErW1tebm5oocDkVFRePj47a2ts0WAOTk5MwVAIkcDesuEs0VAEZGRv///yH5BAEAAA8ALAAAAAAMAAwAAARB8MnnqpuzroZYzQvSNMroUeFIjornbK1mVkRzUgQSyPfbFi/dBRdzCAyJoTFhcBQOiYHyAABUDsiCxAFNWj6UbwQAOw== &quot;);" href="magnet:?xt=urn:btih:$btih&amp;dn=$dn&amp;tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&amp;tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&amp;tr=udp%3A%2F%2Ftracker.istole.it%3A6969&amp;tr=udp%3A%2F%2Ftracker.ccc.de%3A80" title="Get this torrent"> Get this torrent</a>
	</div>
"""

upper = upper.replace('$title', title)
upper = upper.replace('"$type"', '"' + category + '"')
upper = upper.replace('$typestr', categorystr)
upper = upper.replace('$files', files)
upper = upper.replace('$size', size)
upper = upper.replace('$imdb_html', imdb_html)
upper = upper.replace('$spoken', spoken)
upper = upper.replace('$texted', texted)
upper = upper.replace('$tags', tags)
upper = upper.replace('$qualityplus', qualityplus)
upper = upper.replace('$qualityminus', qualityminus)
upper = upper.replace('$qualitytotal', qualitytotal)
upper = upper.replace('$uploaded', uploaded)
upper = upper.replace('$by', by)
upper = upper.replace('$icontag', icons[usertype])
upper = upper.replace('$seeders', seeders)
upper = upper.replace('$leechers', leechers)
upper = upper.replace('$commentamount', unicode(commentamount))
upper = upper.replace('$btih', btih)
upper = upper.replace('$dn', dn)
if picture == '':
	upper = upper.replace('$picturetag', "No picture")
else:
	upper = upper.replace('$picturetag', u'<img src="$picture" title="picture" alt="picture">'.replace('$picture', picture))
upper = upper.replace('$capturedate', capturedate)

middle = u"""	<div class="nfo">
<pre>$description</pre>
	</div>
<br>
	<div class="download">
		<a style="background-image: url(&quot data:image/gif;base64,R0lGODlhDAAMALMPAOXl5ewvErW1tebm5oocDkVFRePj47a2ts0WAOTk5MwVAIkcDesuEs0VAEZGRv///yH5BAEAAA8ALAAAAAAMAAwAAARB8MnnqpuzroZYzQvSNMroUeFIjornbK1mVkRzUgQSyPfbFi/dBRdzCAyJoTFhcBQOiYHyAABUDsiCxAFNWj6UbwQAOw== &quot;);" href="magnet:?xt=urn:btih:$btih&amp;dn=$dn&amp;tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&amp;tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&amp;tr=udp%3A%2F%2Ftracker.istole.it%3A6969&amp;tr=udp%3A%2F%2Ftracker.ccc.de%3A80" title="Get this torrent"> Get this torrent</a>
	</div>"""

middle = middle.replace('$description', unicode(description_text.decode('utf-8')))
middle = middle.replace('$btih', btih)
middle = middle.replace('$dn', dn)

filelist_template = u"""<div id="filelistContainer" style="display: block;"><div style="background:#FFFFFF none repeat scroll 0%clear:left;margin:0;min-height:0px;padding:0;width:100%;">
<table style="border:0pt none;width:100%;font-family:verdana,Arial,Helvetica,sans-serif;font-size:11px;">
	<tbody>
$filetable
	</tbody>
</table>
</div>
</div>"""

if filelist_file_exists:
	file_entry_template = u'\t\t<tr><td align="left">$filename</td><td align="right">$size</td></tr>'

	filetable_list = []
	for file_entry in filelist_rows:
		filetable_list.append(file_entry_template.replace('$filename', file_entry[0]).replace('$size', file_entry[1] + ' ' + file_entry[2]))
	filetable = '\n'.join(filetable_list)

	filelist = filelist_template.replace('$filetable', filetable)
else:
	filelist = filelist_template.replace('$filetable', '')

comments_section_template = u"""</div>
	<div id="commentsheader" class="comments">
	<h4>Comments</h4>
	</div>
	<div id="comments">
	$commententries
	</div>"""

comment_entry_template = u"""<div id="comment-$commentnumber">
<p class="byline">
 <a href="" title="">$commenter</a> at $commentdate:
</p>
<div class="comment">
$commenttext
</div>
</div>"""

if comments_file_exists:
	comment_entry_list = []
	for i, comment in enumerate(comments_rows):
		comment_time = datetime.strptime(comment[1].decode('utf-8'), '%Y-%m-%dT%H:%MZ')
		comment_entry_list.append(comment_entry_template.replace(u'$commentnumber', unicode(i+1)).replace(u'$commenter', unicode(comment[0].decode('utf-8'))).replace(u'$commentdate', unicode(comment_time.strftime("%Y-%m-%d %H:%M GMT"))).replace(u'$commenttext', unicode(comment[2].decode('utf-8'))))
	commententries = '\n'.join(comment_entry_list)

	comments_section = comments_section_template.replace('$commententries', commententries)
else:
	comments_section = u"""<div id="comments"></div>
</div>"""

footer = u"""</div>
</div>
<div id="foot" style="text-align:center;margin-top:1em;">
<p id="footer" style="color:#666; font-size:0.9em; ">
        Captured: $capturedate<br>
        ID: $torrent_id
</p>
	</div>
</body></html>""".replace(u'$capturedate', capturedate).replace('$torrent_id', unicode(torrent_id))

codecs.open('output/' + str(torrent_id) + '.html', 'w', 'utf-8').write(upper + middle + filelist + comments_section + footer)
