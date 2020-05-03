import csv
import os
import sys
from google_images_download import google_images_download

if __name__ == "__main__":
    bird_eng_names = []
    bird_img_count = []

    with open('report.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            bird_eng_names.append(row[0])
            bird_img_count.append(int(row[1]))

    n_birds = len(bird_eng_names)

    chromedriver_path = os.environ["CHROME_DRIVER_PATH"];
    for i in range(n_birds):
        if bird_img_count[i] < 400:
            response = google_images_download.googleimagesdownload()
            arguments = {'keywords': bird_eng_names[i],
                         "limit": 500,
                         'chromedriver': chromedriver_path,
                         'output_directory': 'images/',
                         'save_source': 'sources',
                         'extract_metadata': True}
            paths = response.download(arguments)
