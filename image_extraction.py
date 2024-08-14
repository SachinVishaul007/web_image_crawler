import requests
from bs4 import BeautifulSoup
import imageio
import cairosvg
from PIL import Image
from io import BytesIO
import re
import sys
import time



def spinner(duration=100):
    spinner_chars = ['|', '/', '-', '\\']
    end_time = time.time() + duration

    while time.time() < end_time:
        for char in spinner_chars:
            sys.stdout.write(f'\r{char} Extracting Images...')
            sys.stdout.flush()
            time.sleep(0.1)  

spinner()

url = 'https://www.incredibleindia.org/content/incredible-india-v2/en.html'
base_url = 'https://www.incredibleindia.org'

response = requests.get(url)

def convert_svg_to_png(svg_bytes):
    try:
        return cairosvg.svg2png(bytestring=svg_bytes)
    except Exception as e:
        print(f"Error converting SVG: {e}")
        return None


def is_large_image(image_url):
    try:

        response = requests.get(base_url + image_url, timeout=10)

        image_format = image_url.split('.')[-1].lower()
        image_bytes = BytesIO(response.content)

        if image_format == 'svg':
            png_data = convert_svg_to_png(image_bytes.getvalue())
            if png_data:
                image_bytes = BytesIO(png_data)
                image = Image.open(image_bytes)
        else:
            image = Image.open(image_bytes)

        width, height = image.size
        return width >= min_width and height >= min_height

    except Exception as e:
        print(f"Error with image {image_url}: {e}")
        return False

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img.get('data-src') for img in img_tags if img.get('data-src')]
    
    min_width, min_height = 100,100

    large_img_urls = [url for url in img_urls if is_large_image(url)]

    for large_img_url in large_img_urls:
        print(large_img_url)
    print("for min filter:" + str(min_width) + "x" + str(min_height) + " -----> count: " + str(len(large_img_urls)))

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")







