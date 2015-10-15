# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 13:41:28 2015

@author: wly
"""

import logging
from time import time

from .download import get_tokenDict,setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

def main():
   #These three parameters are user defined
   client_id = '*****'
   username='***'
   password='*****'
   
   tokenDict=get_tokenDict(client_id, username,password)
   
   ts = time()
   download_dir = setup_download_dir()
   links = [l for l in get_links(client_id,tokenDict) if l.endswith('.jpg')]
   for link in links:
       download_link(download_dir, link)
   print('Took {}s'.format(time() - ts))

if __name__ == '__main__':
   main()
