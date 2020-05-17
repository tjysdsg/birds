import os
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--list-file', help='File containing a list of image files', nargs='?', type=str)
    parser.add_argument('--output', help='Output file name excluding extension', nargs='?', type=str, default='report')
    args = parser.parse_args()
    output_file = args.output
    list_file = args.list_file
    bird_eng_names = []

    # map original filename to filtered filename
    orig2filtered_raw: dict = json.load(open("orig2filtered.json"))
    orig2filtered = {}
    for k, v in orig2filtered_raw.items():
        k = os.path.basename(k)
        orig2filtered[k] = v

    os.makedirs("filtered_logs", exist_ok=True)
    for bird_cat in os.listdir("logs"):
        filtered_log = {}
        log: dict = json.load(open(os.path.join("logs", bird_cat)))
        for f in log:
            orig_key = f['image_filename']
            if orig_key not in orig2filtered:
                continue
            filename = orig2filtered[orig_key]
            f['image_filename'] = filename
            filtered_log[filename] = f['image_link']
        json.dump(filtered_log, open(os.path.join("filtered_logs", bird_cat), "w"))
