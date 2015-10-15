# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 07:07:34 2015

@author: wly
"""
import logging
from time import time

from .download import get_tokenDict,setup_download_dir, get_links, download_link
from queue import Queue
from threading import Thread
from sys import argv


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


class DownloadWorker(Thread):
   def __init__(self, queue):
       Thread.__init__(self)
       self.queue = queue

   def run(self):
       while True:
           # Get the work from the queue and expand the tuple
           directory, link = self.queue.get()
           download_link(directory, link)
           self.queue.task_done()

def main():
   #These three parameters are user defined
   client_id = '*****'
   username='***'
   password='*****'
   
   tokenDict=get_tokenDict(client_id, username,password)
   
   ts = time()
   download_dir = setup_download_dir()
   links = [l for l in get_links(client_id,tokenDict) if l.endswith('.jpg')]
   # Create a queue to communicate with the worker threads
   queue = Queue()
   # Create worker threads
   
   
   for x in range(int(argv[1])):
       worker = DownloadWorker(queue)
       # Setting daemon to True will let the main thread exit even though the workers are blocking
       worker.daemon = True
       worker.start()
   # Put the tasks into the queue as a tuple
   for link in links:
       logger.info('Queueing {}'.format(link))
       queue.put((download_dir, link))
   # Causes the main thread to wait for the queue to finish processing all the tasks
   queue.join()
   print('Took {}'.format(time() - ts))
   
#to run this on the command line, tpye 
#python -m multithreadDownload-master.multithread numOfThreads  
if __name__ == '__main__':
    
   main()
