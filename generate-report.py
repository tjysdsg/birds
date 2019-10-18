import csv
import os
import sys
from collections import Counter

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Need to specify the location of the dataset")
    img_dir = sys.argv[1]
    bird_eng_names = []
    
    with open('bird_china_map_labeled.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            bird_eng_names.append(row[2])
        del bird_eng_names[0]

    bird_img_count = [0 for _ in bird_eng_names]
    n_birds = len(bird_eng_names)
    for i in range(n_birds):
        bird = bird_eng_names[i]
        bird_dir = os.path.join(img_dir, bird)
        if os.path.isdir(bird_dir):
            bird_img_count[i] = len(os.listdir(bird_dir))

    counter = Counter(bird_img_count)
    # write report
    with open('report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(n_birds):
            writer.writerow([bird_eng_names[i], bird_img_count[i]])

    with open('n_images_count.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        n_counters = len(counter.keys())
        for i in range(n_counters):
            writer.writerow([list(counter.keys())[i], list(counter.values())[i]])
