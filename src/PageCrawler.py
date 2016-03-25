__author__ = 'luocheng'

pages = []
import os
import sys
import random

reload(sys)
sys.setdefaultencoding( "utf-8" )
from selenium import webdriver


while True:
    try:
        finished = os.listdir('../data/screenshots')
        for l in open('../data/url.tsv'):
            globalid, _, _, url = l.strip().split('\t')
            if globalid + '.png' not in finished:
                pages.append((globalid, url))
        random.shuffle(pages)
        for item in pages:
            globalid = item[0]
            url = item[1]
            browser = webdriver.Firefox()
            browser.set_script_timeout(30)
            browser.set_page_load_timeout(30)
            browser.implicitly_wait(30)
            try:
                browser.get(url)
                browser.get_screenshot_as_file('../data/screenshots/'+str(globalid)+'.png')
                print 'Success', globalid,len(pages)
            except:
                import sys
                print  sys.exc_info()[0]
                print 'Failure',len(pages), globalid, url
            finally:
                # file = open('../data/pages/' + globalid + '.html', 'w')
                # file.write(browser.page_source)
                # file.close()
                browser.quit()

        # finished = os.listdir('../data/pages')
        # for item in finished:
        #     size = os.path.getsize('../data/pages/' + item)
        #     if size < 10 * 1024:
        #         os.system("rm ../data/pages/" + item)
        #         print 'REMOVE ' + item

    except:
        print 'BEGIN Again!'