import os
from urllib.request import Request, urlopen
import urllib
import urllib.request
import urllib.parse
import re
try:
    from urlparse import urljoin  # Python2
except ImportError:
    from urllib.parse import urljoin  # Python3
from bs4 import BeautifulSoup
from general import *
from domain import *

IMAGE_TYPES = ['.gif', 'jpeg']#, '.jpeg'

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def is_absolute(url):
    return bool(urlparse(url).netloc)

# setting up
def make_soup(url):
    #thepage = urllib.request.urlopen(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    thepage = urlopen(req)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

def download_images(page_url):
    project_name = get_domain_name(page_url)
    project_name = os.path.join(project_name, "images")
    create_project_dir(project_name)
    i=1
    soup = make_soup(page_url)
    for img in soup.find_all('img'):
    #for img in soup.find_all('img', src=re.compile('.\S*.gif')):
        temp = img.get('src')
        if is_absolute(temp):
            image = temp
        else:
            image = urljoin(page_url, temp)
        #print(" Downloading " + image)

        description = img.get('alt')
        if description == None:
            description = page_url[-12:] + "_" + str(i)
            i += 1
        else:
            description = page_url[-12:] + "_" + description
        description = description.replace('/','_')
        description = description.replace('.', '_')
        description = description.replace('\\', '_')
        description = description.replace('html', '_')
        filename = os.path.join(project_name, description)
        imagefile = open(filename + ".gif", 'wb')
        req = Request(image, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req).read()
        #opener = AppURLopener()
        #res = opener.open(image)
        #response = res.read()
        imagefile.write(response)
        imagefile.close()
