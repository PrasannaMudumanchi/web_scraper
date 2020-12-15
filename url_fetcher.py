# problem statement
# take a url and get all the urls in that page along with link keywords and save it in csv file
# improve it to fetch image links and social media account links

import requests
import re
import json
import csv
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def isValidUrl(url):
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
             )
    pattern = re.compile(regex)

    if (url == None):
        return False

    if (re.search(pattern, url)):
        return True
    else:
        return False


def get_website_url(url):
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}"
             )
    pattern_url = re.compile(regex)
    result = re.search(pattern_url, url)
    return result.group()


def fetch_url(main_url, fileType):
    req = requests.get(main_page_url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    page_urls = soup.find_all("a")
    if fileType == "csv":
        fetch_url_csv(page_urls)
    elif fileType == "json":
        fetch_url_json(page_urls)
    else:
        print("Invalid fileType")


def fetch_url_csv(page_urls):
    with open('page_links.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["text", "link"])
        for url in page_urls:
            url_text = url.get_text()
            ref = url.get('href')
            if ref is not None and ref.startswith('/'):
                ref = str(get_website_url(main_page_url)) + ref
            elif ref is not None and ref.startswith('#'):
                ref = str(main_page_url)+ref
            writer.writerow([url_text, ref])
    f.close()


def fetch_url_json(page_urls):
    data = {}
    data['page_urls'] = []
    for url in page_urls:
        url_dict = {}
        url_dict['text'] = url.get_text()
        ref = url.get('href')
        if ref is not None and ref.startswith('/'):
            ref = str(get_website_url(main_page_url)) + ref
        elif ref is not None and ref.startswith('#'):
            ref = str(main_page_url)+ref
        url_dict['link'] = ref
        data['page_urls'].append(url_dict)

    # print(soup.prettify())
    with open('page_links.json', 'w') as f:
        json.dump(data, f)
    f.close()


def fetch_images():
    pass


if __name__ == '__main__':
    main_page_url = input()
    fileType = input("Enter FileType: ")
    if (main_page_url):
        fetch_url(main_page_url, fileType)
