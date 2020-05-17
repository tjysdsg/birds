# 中国鸟类图片数据集

## 数据来源

来源于Google Images, 用这个[脚本](https://github.com/tjysdsg/birds/blob/master/selective-download.py)下载的

NOTE: you need to download chromedriver executable, and set the path to
`CHROME_DRIVER_PATH` environment variable to run the script.

## 筛选

使用了预先训练好的[mobilenet\_v2](https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1) 来自动筛选掉不包含鸟的图片, 并裁剪包含鸟的图片

代码在这里: [auto-filter-data.ipynb](https://github.com/tjysdsg/birds/blob/master/auto-filter-data.ipynb)

## 数据集结构

- `bird_china_map_labeled.csv`: 每种鸟类别的信息, 如英文名、中文名、稀有度等。 *有些类别缺少数据*
- `bird_images.tar.gz`: gzip压缩包, 包含如下文件夹结构:
    - 数据集根目录
        - 鸟类名字1
            - 图片1
            - 图片2
            - 图片3
            - ...
            - 图片n
        - 鸟类名字2
            - 图片1
            - 图片2
            - 图片3
            - ...
            - 图片n
        - ...
        - 鸟类名字N
            - 图片1
            - 图片2
            - 图片3
            - ...
            - 图片n
- `archive.txt`: 包含所有图片(相对于数据集根目录)的文件路径
- `filtered_logs/`: 所有图片的文件名, 对应的源网址。每个json文件都有如下格式:
    ```
    {
        图片文件名1: 网址1,
        图片文件名2: 网址2,
        ...
        图片文件名n: 网址n
    }
    ```
    子文件夹:
    - 鸟类名字1.json
    - 鸟类名字2.json
    - ...
    - 鸟类名字N.json
