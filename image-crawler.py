# -*- coding: utf-8 -*-
import sys
import os
import urllib.request
from urllib.parse import quote
import http.client
from http.client import IncompleteRead, BadStatusLine
import ssl
from urllib.request import URLError, HTTPError
import json
import time

http.client._MAXHEADERS = 1000


def download_page(url):
    """Downloading entire Web Document (Raw Page Content)
    """
    try:
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36" \
                            " (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print("Could not open URL. Please check your internet connection and/or ssl settings \n"
              "If you are using proxy, make sure your proxy settings is configured correctly")
        sys.exit()


def build_search_url(search_term, params):
    """Building main search URL
    """
    # check the args and choose the URL
    url = 'https://www.google.com/search?q=' + quote(
        search_term.encode(
            'utf-8')) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

    return url


def build_url_parameters():
    """Building URL parameters
    """
    lang_url = ''
    time_range = ''
    exact_size = ''

    built_url = "&tbs="
    built_url = lang_url + built_url + exact_size + time_range
    return built_url


# Finding 'Next Image' from the given raw page
def get_next_image_item(raw_html):
    start_line = raw_html.find('rg_meta notranslate')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = raw_html.find('class="rg_meta notranslate">')
        start_object = raw_html.find('{', start_line + 1)
        end_object = raw_html.find('</div>', start_object + 1)
        object_raw = str(raw_html[start_object:end_object])
        # remove escape characters
        try:
            object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
            final_object = json.loads(object_decode)
        except:
            final_object = ""
        return final_object, end_object


def get_all_image_items(page, main_directory, dir_name, limit):
    """Getting all links for images
    """
    items = []
    abs_path = []
    errorCount = 0
    i = 0
    count = 1
    while count < limit + 1:
        object, end_content = get_next_image_item(page)
        if object == "no_links":
            break
        elif object == "":
            page = page[end_content:]
        else:
            # format the item for readability
            formatted_object = {}
            formatted_object['image_format'] = object['ity']
            formatted_object['image_height'] = object['oh']
            formatted_object['image_width'] = object['ow']
            formatted_object['image_link'] = object['ou']
            formatted_object['image_description'] = object['pt']
            formatted_object['image_host'] = object['rh']
            formatted_object['image_source'] = object['ru']
            formatted_object['image_thumbnail_url'] = object['tu']
            object = formatted_object

            # download the images
            download_status, download_message, return_image_name, absolute_path = download_image(
                object['image_link'], object['image_format'], main_directory, dir_name, count)
            if download_status == "success":
                count += 1
                object['image_filename'] = return_image_name
                items.append(object)  # Append all the links in the list named 'Links'
                abs_path.append(absolute_path)
            else:
                errorCount += 1

            page = page[end_content:]
        i += 1
    if count < limit:
        print("=" * 80)
        print("Unfortunately all " + str(
            limit) + " could not be downloaded because some images were not downloadable. " + str(
            count - 1) + " is all we got for this search filter!")
    return items, errorCount, abs_path


# Download Images
def download_image(image_url, image_format, main_directory, dir_name, count):
    try:
        req = urllib.request.Request(image_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        try:
            # timeout time to download an image
            timeout = 10

            response = urllib.request.urlopen(req, None, timeout)
            data = response.read()
            response.close()

            extensions = [".jpg", ".jpeg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico"]
            # keep everything after the last '/'
            image_name = str(image_url[(image_url.rfind('/')) + 1:])
            if format:
                if not image_format or image_format != format:
                    download_status = 'fail'
                    download_message = "Wrong image format returned. Skipping..."
                    return_image_name = ''
                    absolute_path = ''
                    return download_status, download_message, return_image_name, absolute_path

            if image_format == "" or not image_format or "." + image_format not in extensions:
                download_status = 'fail'
                download_message = "Invalid or missing image format. Skipping..."
                return_image_name = ''
                absolute_path = ''
                return download_status, download_message, return_image_name, absolute_path
            elif image_name.lower().find("." + image_format) < 0:
                image_name = image_name + "." + image_format
            else:
                image_name = image_name[:image_name.lower().find("." + image_format) + (len(image_format) + 1)]

            prefix = ''

            path = main_directory + "/" + dir_name + "/" + prefix + str(count) + "." + image_name

            try:
                output_file = open(path, 'wb')
                output_file.write(data)
                output_file.close()
                absolute_path = os.path.abspath(path)
            except OSError as e:
                download_status = 'fail'
                download_message = "OSError on an image...trying next one..." + " Error: " + str(e)
                return_image_name = ''
                absolute_path = ''
                return download_status, download_message, return_image_name, absolute_path

            # return image name back to calling method to use it for thumbnail downloads
            download_status = 'success'
            download_message = "Completed Image ====> " + prefix + str(count) + "." + image_name
            return_image_name = prefix + str(count) + "." + image_name

        except UnicodeEncodeError as e:
            download_status = 'fail'
            download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        except URLError as e:
            download_status = 'fail'
            download_message = "URLError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

        except BadStatusLine as e:
            download_status = 'fail'
            download_message = "BadStatusLine on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''
            absolute_path = ''

    except HTTPError as e:  # If there is any HTTPError
        download_status = 'fail'
        download_message = "HTTPError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''
        absolute_path = ''

    except URLError as e:
        download_status = 'fail'
        download_message = "URLError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''
        absolute_path = ''

    except ssl.CertificateError as e:
        download_status = 'fail'
        download_message = "CertificateError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''
        absolute_path = ''

    except IOError as e:  # If there is any IOError
        download_status = 'fail'
        download_message = "IOError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''
        absolute_path = ''

    except IncompleteRead as e:
        download_status = 'fail'
        download_message = "IncompleteReadError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''
        absolute_path = ''

    return download_status, download_message, return_image_name, absolute_path


# Download Page for more than 100 images
def download_extended_page(url, chromedriver):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")

    try:
        browser = webdriver.Chrome(chromedriver, chrome_options=options)
    except Exception as e:
        print("Cannot find chromedriver(exception: %s)" % e)
        sys.exit()
    browser.set_window_size(1024, 768)

    # Open the link
    browser.get(url)
    time.sleep(1)
    element = browser.find_element_by_tag_name("body")

    failed_count = 0
    # Scroll down
    while failed_count < 50:
        for _ in range(30):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        time.sleep(5)
        try:
            browser.find_element_by_id("smb").click()
        except:
            failed_count += 1
            print("Cannot find 'Show More Results' button, retrying")
        print(browser.page_source)

    print("Reached end of Page.")

    source = browser.page_source  # page source
    # close the browser
    browser.close()

    return source


if __name__ == "__main__":
    main_directory = './'
    dir_name = 'images'
    limit = 500
    search_term = 'AA'
    chromedriver = '/home/tjy/repos/birds/chromedriver'

    print("Building url parameters")
    params = build_url_parameters()  # building URL with params
    print("Building search url")
    url = build_search_url(search_term, params)  # building main search url
    print("URL for search page:", url)
    print("Downloading search html")
    # raw_html = download_page(url)  # download page
    raw_html = download_extended_page(url, chromedriver)
    print("Getting image links")
    items, errorCount, abs_path = get_all_image_items(raw_html, main_directory, dir_name,
                                                      limit)  # get all image items and download images
