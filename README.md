# China's Bird Images

## Data

Original data was retrieved from Google Images, using [this script](https://github.com/tjysdsg/birds/blob/master/selective-download.py).

NOTE: you need to download chromedriver executable, and set the path to
`CHROME_DRIVER_PATH` environment variable to run the script.

## Filtering

The filtering is automated using tensorflow's [pretrained mobilenet\_v2](https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1).
The filtering code is in [auto-filter-data.ipynb](https://github.com/tjysdsg/birds/blob/master/auto-filter-data.ipynb).
