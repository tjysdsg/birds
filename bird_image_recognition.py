# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
bird_names = pd.read_csv('bird_names.csv')
bird_names = bird_names.values.flatten().tolist()
print(bird_names)
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()
last_keyword = ''
for k in bird_names:
  arguments = {'keywords':k, "limit": 500,'chromedriver':'E:\\bird-image-recognition\\chromedriver.exe', 'output_directory':'images/','save_source':'sources','extract_metadata':True}
  paths = response.download(arguments)
  last_keyword = k
print(last_keyword)

