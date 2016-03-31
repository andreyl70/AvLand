# -*- coding: utf-8 -*-

import sys, os
from selenium import webdriver
import time
import random
import json
import requests
import re

kMosOblPt = ("55.8","37.4")
kKalugaOblPt = ("54.3718","35.445185")
kKaliningradOblPt = ("54.754365","21.22993")
kSleepRange = [10, 30]

def LOG(msg):
    print msg,
    sys.stdout.flush()

def sleepAfterClick():
    sleep_sec = random.randrange(*kSleepRange)
    LOG("Sleeping: {0} seconds...".format(sleep_sec))
    time.sleep(sleep_sec)
    LOG("OK\n")

def get_ya_coord(addr_str, center_pt):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {'geocode':addr_str, 'll': ','.join(center_pt), 'spn':'3.,3,', 'results':'1', 'format':'json'}
    resp = requests.get(url, params=params)
    raw_js = json.loads(resp.text)
    try:
        members = raw_js['response']['GeoObjectCollection']['featureMember']
        if members:
            lon, lat = members[0]['GeoObject']['Point']['pos'].split()
            return u"{0},{1}".format(lat, lon)
    except Exception, ex:
        LOG("ERROR: '{0}'\n".format(ex))

def crawl(start_url, out_path):
    def _extract_href(root):
        elems = root.find_elements_by_xpath('h3[@class="title"]/a')
        if elems:
            return elems[0].get_attribute('href')

    def _extract_title(root):
        elems = root.find_elements_by_xpath('h3[@class="title"]/a')
        if elems:
            return elems[0].get_attribute('title')

    def _extract_price(root):
        """ return 'None' or integer value """
        elems = root.find_elements_by_xpath('div[@class="about"]')
        if elems:
            digit_parts = re.findall(r'\d+', elems[0].text.strip())                                        
            try:
                return int(u"".join(digit_parts))
            except Exception, ex:
                LOG("Error: '{0}'\n".format(ex))

    def _extract_agent(root):
        elems = root.find_elements_by_xpath('div[@class="data"]/p')
        if elems:
            return u" ".join([e.text for e in elems]).strip()

    def _extract_date(root):
        elems = root.find_elements_by_xpath('div[@class="data"]/div[@class="date c-2"]')
        if elems:
            return elems[0].text.strip()

    def _extract_address(root):
        elems = root.find_elements_by_xpath('//div[@class="description_content"]/span[@id="toggle_map"]/span')
        if elems:
            return u" ".join([e.text for e in elems]).strip()

    def _extract_description(root):
        elems = root.find_elements_by_xpath('//div[@class="description description-expanded"]/div[@class="item-params c-1"]')
        if elems:
            return u" ".join([e.text for e in elems]).strip()

    def _extract_comments(root):
        elems = root.find_elements_by_xpath('//div[@class="description description-text"]')
        if elems:
            return u" ".join([e.text for e in elems]).strip()

    def _extract_id(root):
        elems = root.find_elements_by_xpath('//div[@class="item-sku"]/span[@id="item_id"]')
        if elems:
            return int(elems[0].text.strip())
    #=======================================================

    browser = webdriver.Firefox()
    browser.implicitly_wait(10) 
    log_file = open(out_path, 'w')

    try:
        browser.get(start_url)

        while True:
            next_page = browser.find_element_by_partial_link_text("Следующая страница")
            if next_page:
                next_page = next_page.get_attribute('href')

            items = []
            for root in browser.find_elements_by_xpath('//div[@class="description"]'):
                item = {}
                item['href'] = _extract_href(root)
                item['title'] = _extract_title(root)
                item['price'] = _extract_price(root)
                item['agent'] = _extract_agent(root)
                item['date'] = _extract_date(root)
                items.append(item)

            for item in items:
                browser.get(item['href'])
                sleepAfterClick()

                item['address'] = _extract_address(browser)
                item['description'] = _extract_description(browser)
                item['comments'] = _extract_comments(browser)
                item['id'] = _extract_id(browser)
                item['coord'] = get_ya_coord(item['address'], kKalugaOblPt)

                print >> log_file, json.dumps(item, ensure_ascii=False).encode('utf8')

            if not next_page:
                break

            LOG("{0} items saved\n".format(len(items)))
            browser.get(next_page)
            sleepAfterClick()
    finally:
        browser.quit()

#=================================================
if __name__ == "__main__":
    crawl(sys.argv[1], sys.argv[2])
