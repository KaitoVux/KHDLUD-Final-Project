from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import csv

browser = webdriver.Chrome()
browser.maximize_window()

def crawlAllComment(url):
    records = []
    browser.get(url)
    # tat quang cao
    browser.find_element_by_css_selector('html').send_keys(Keys.ESCAPE)

    # scroll
    time.sleep(1)
    total_height = int(browser.execute_script(
        "return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        browser.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(3)

    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    
    #tat dialog
    button = browser.find_elements_by_css_selector(
        'button.align-right.secondary.slidedown-button')

    if(len(button) > 0):
        button[0].click()

    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    commentDivs = soup.findAll(
        "div", {"class": "style__StyledComment-sc-103p4dk-5 dDtAUu review-comment"})
    for commentDiv in commentDivs:
        cmt = commentDiv.find(
            "div", {"class": "review-comment__content"}).text
        if(len(cmt) > 0):
            records.append(cmt)

    navigationButton = browser.find_elements_by_css_selector(
        'a.btn.next')

    while len(navigationButton) > 0:
        navigationButton[0].click()
        time.sleep(1)
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        commentDivs = soup.findAll(
            "div", {"class": "style__StyledComment-sc-103p4dk-5 dDtAUu review-comment"})
        for commentDiv in commentDivs:
            cmt = commentDiv.find(
                "div", {"class": "review-comment__content"}).text
            if(len(cmt) > 0):
                records.append(cmt)
        navigationButton = browser.find_elements_by_css_selector(
            'a.btn.next')

    return records

def crawlComment(url):
    records = []
    browser.get(url)
    # tat quang cao
    browser.find_element_by_css_selector('html').send_keys(Keys.ESCAPE)

    # scroll
    time.sleep(1)
    total_height = int(browser.execute_script(
        "return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        browser.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(3)

    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    button = browser.find_elements_by_css_selector(
        'button.align-right.secondary.slidedown-button')
    if(len(button) > 0):
        button[0].click()

    button = browser.find_elements_by_css_selector(
        'div.filter-review__item')

    if(len(button) > 0):
        button[3].click()
        time.sleep(1)

        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        commentDivs = soup.findAll(
            "div", {"class": "style__StyledComment-sc-103p4dk-5 dDtAUu review-comment"})
        for commentDiv in commentDivs:
            cmt = commentDiv.find(
                "div", {"class": "review-comment__content"}).text
            title = commentDiv.find(
                "a", {"class": "review-comment__title"}).text
            record = {'comment': title+', '+cmt, 'is_trust': 1}
            print(record)
            records.append(record)

        button[3].click()
        button[6].click()
        button[7].click()
        time.sleep(1)

        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        commentDivs = soup.findAll(
            "div", {"class": "style__StyledComment-sc-103p4dk-5 dDtAUu review-comment"})

        for commentDiv in commentDivs:
            cmt = commentDiv.find(
                "div", {"class": "review-comment__content"}).text
            title = commentDiv.find(
                "a", {"class": "review-comment__title"}).text
            record = {'comment': title+', '+cmt, 'is_trust': 0}
            print(record)
            records.append(record)

    return records

def getProductDetailUrl(url):
    browser.get(url)
    # tat quang cao
    browser.find_element_by_css_selector('html').send_keys(Keys.ESCAPE)

    button = browser.find_elements_by_css_selector(
        'div.slick-slide.slick-active')
    button[1].click()

    # scroll
    time.sleep(1)
    total_height = int(browser.execute_script(
        "return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        browser.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(1)

    time.sleep(1)
    total_height = int(browser.execute_script(
        "return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        browser.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(1)

    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    productDiv = soup.find(
        "div", {"data-view-id": "product_container"})

    hrefs = productDiv.findAll('a')

    urls = []
    for href in hrefs:
        urls.append(href.get('href'))
        print(href.get('href'))

    return urls


productUrls = getProductDetailUrl('https://tiki.vn/deal-hot?tab=now&page=1')

fieldList = ['comment', 'is_trust']

try:
    with open('khdl_final_final6.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldList)
        writer.writeheader()
        for productUrl in productUrls:
            records = crawlComment(productUrl)
            for record in records:
                print(record)
                writer.writerow(
                    {'comment': record['comment'], 'is_trust': record['is_trust']})
except IOError:
    print("I/O error")

browser.quit()
