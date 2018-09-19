#!/usr/bin/env python
###          daddycocoaman     ###
###  https://daddycocoaman.com ###
###  http://twitter.com/mcohmi ###

from __future__ import print_function

import argparse
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def getLinks(url):
    sess = requests.Session()
    page = sess.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    links = [(link.string, link['href']) for link in soup.find_all('a', href=True) if link['href'].startswith("/downloader.php?key1")]
    return links

def downloadFiles(links, outdir, url):
    domain = "https://www.jeejuh.com"
    
    for name, link in links:
        trackName = name.split("-")[1].strip().rstrip()
        path = os.path.join(outdir,trackName)
        if not os.path.exists(path):
            os.mkdir(path)

        sess = requests.Session()
        wavURL = sess.get(domain + link, headers={'referer': url})
        print ("Saving " + name + " to " + os.path.join(path,name) + "...")
        with open(os.path.join(path,name), "wb") as curWav:
            curWav.write(wavURL.content)

def main():
    parser = argparse.ArgumentParser(description="Downloads WAV files and PDFs from download link pages provided by JeeJuh.com.")
    parser.add_argument('URL', help="URL of download page. Enclose URL in quotes.")
    parser.add_argument('-O', '--output-dir', help="Output directory", metavar="")
    args = parser.parse_args()

    if args.output_dir:
        outdir = args.output_dir
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    else:
        outdir = os.getcwd()
  
    links = getLinks(args.URL)
    downloadFiles(links, outdir, args.URL)

    print ("Complete!")

if __name__ == '__main__':
    main()