# Bird image recognition using tensorflow

# Datasets

Original data was retrieved from Google Image. Each bird category contains around 500 images. The detailed information of each bird category is in [report.csv](report.csv).

## Data Filtering

The filtering is automated using tensorflow's [pretrained model](https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1). The filtering code is in [auto-filter-data.ipynb](auto-filter-data.ipynb).

## Data Augmentation

Training data is augmented using tensorflow's ImageDataGenerator (see [notebook](bird-image-recognition.ipynb)):

```python
image_gen_train = ImageDataGenerator(
                    rotation_range=45,
                    width_shift_range=0.2,
                    height_shift_range=0.2,
                    horizontal_flip=True,
                    shear_range=0.2,
                    zoom_range=0.1)
```

# Training

First 10 categories of birds were trained [here](bird-image-recognition.ipynb). 