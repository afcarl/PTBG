__author__ = 'luocheng'

pages = []
import os

while True:
    finished = os.listdir('../data/pages')
    for l in open('../data/url.tsv'):
        globalid, _, _, url = l.strip().split('\t')
        if globalid + '.html' not in finished:
            pages.append((globalid, url))
        else:
            print 'SKIP', globalid
    for item in pages:
        globalid = item[0]
        url = item[1]
        try:
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
            import urllib2
            r = urllib2.Request(url, headers=headers)
            f = urllib2.urlopen(url, timeout=30)
            html = f.read()
            file = open('../data/pages/' + globalid + '.html', 'w')
            file.write(html)
            file.close()
            print 'Success', globalid
        except:
            import sys

            print  sys.exc_info()[0]
            print 'Failure', globalid, url
    finished = os.listdir('../data/pages')
    for item in finished:
        size = os.path.getsize('../data/pages/' + item)
        if size < 10 * 1024:
            os.system("rm ../data/pages/" + item)
            print 'REMOVE ' + item
