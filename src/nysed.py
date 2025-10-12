import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
import os
from src.mdb_tools import Mdb



def scrape_nysed(url="https://data.nysed.gov/downloads.php"):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    zip_links = []
    for lnk in soup.find_all('a'):
        data = lnk.get('href')
        if data.endswith('.zip'):
            zip_links.append(data)
    return zip_links

def download_and_process_zip(filepath, baseurl = "https://data.nysed.gov"):
    url = baseurl + filepath
    print("Downloading " + url)
    response = requests.get(url)
    zip_data = BytesIO(response.content)
    pandas = {}
    with ZipFile(zip_data) as zf:
        print("Unzipping data")
        seen = []
        for filename in zf.namelist():
            if filename.endswith('.accdb') or filename.endswith('.mdb'):
                woext = os.path.splitext(filename)[0]
                if woext in seen:
                    continue
                else:
                    seen.append(woext)
                print("Found mdb file " + filename)
                with TemporaryDirectory() as tmpdir:
                    mdb_file = zf.extract(filename, path=tmpdir)
                    print ("Processing " + mdb_file)
                    tables = Mdb(mdb_file).panda_tables()
                    for n,t in tables.items():
                        print("Found table " + n + " in " + filename)
                        pandas[n] = t
    return pandas


def save_panda_tables(dict, name_to_path):
    for n,t in dict.items():
        path = name_to_path(n) + ".pkl"
        print("saving to " + path)
        t.to_pickle(path)


def get_data(links = []):
    dir = "./data/nysed"
    if links == []:
        links = scrape_nysed()
    errors = []
    for link in links:
        try: 
            ps = download_and_process_zip(link)
            ldir = dir + "/" + os.path.dirname(link.removeprefix("/files/")).replace("/", "_")
            os.makedirs(ldir, exist_ok=True)
            save_panda_tables(ps, lambda x: ldir + "/" + x.replace("/", "_"))
        except:
            errors.append(link)
    return errors

# The following errored for whatever reason: 
def do_rest():
    links = [
        # "/files/reportcards/16-17/SRC2017.zip",
        "/files/reportcards/15-16/SRC2016.zip",
        "/files/reportcards/14-15/SRC2015.zip",
        "/files/reportcards/13-14/SRC2014.zip",
        "/files/reportcards/12-13/SRC2013.zip",
        "/files/reportcards/archive/2011-12/SRC2012.zip",
        "/files/reportcards/archive/2010-11/SRC2011.zip",
        "/files/reportcards/archive/2009-10/SRC2010.zip",
        "/files/reportcards/archive/2008-09/SRC2009.zip",
        "/files/reportcards/archive/2007-08/SRC2008.zip",
        "/files/reportcards/archive/2006-07/SRC2007.zip",
        "/files/reportcards/archive/2005-06/SRC2006.zip",
    ]
    get_data(links)
