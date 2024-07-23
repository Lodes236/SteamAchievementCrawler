"""
This script downloads achievement images from a specific Steam community page, saves them
in a directory named "achievements", and resizes them to 64x64 pixels.

Modules required:
- bs4 (BeautifulSoup)
- PIL (Pillow)
- os
- requests
- shutil

Steps:
1. Creates a directory named "achievements" in the directory where the script is located.
2. Sends a GET request to the Steam community achievements page for a specific game.
3. Parses the HTML response using BeautifulSoup.
4. Extracts the URLs and names of the achievement images.
5. Downloads each image and saves it in the "achievements" folder.
6. Resizes each image to 64x64 pixels and overwrites the original image.

Classes:
    None

Functions:
    None

Usage:
    Run the script in an environment where the required modules are installed.
"""

from bs4 import BeautifulSoup
from PIL import Image
import os
import requests
import shutil

# Create directory for images
current_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(current_directory, "achievements")

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f'Folder "achievements" created at {folder_path}')
else:
    print(f'Folder "achievements" already exists at {folder_path}')

# Request
r = requests.get("https://steamcommunity.com/stats/1177980/achievements")  # put link to achievements here
html_code = r.text

steam_product = BeautifulSoup(html_code, 'html.parser')

main_contents = steam_product.find('div', id='mainContents')

image_urls = []
image_names = []
counter = 0

# If DOC element is found generate file names
if main_contents:
    achieve_img_holders = main_contents.find_all('div', class_='achieveRow')

    if achieve_img_holders:
        for element in achieve_img_holders:
            raw_imageUrl = str(element)
            imageUrl = raw_imageUrl.split("src=\"")
            imageUrl = imageUrl[1].split("\" width")
            realUrl = imageUrl[0]

            image_urls.append(realUrl)

        for element in achieve_img_holders:
            raw_imageName = str(element)
            imageName = raw_imageName.split("<h3>")
            imageName = imageName[1].split("</h3>")
            realName = imageName[0]
            image_names.append(realName)

    else:
        print("Keine Elemente mit der Klasse 'achieveImgHolder' gefunden.")
else:
    print("DIV mit der ID 'mainContents' nicht gefunden.")

# Download, rename, save and resize the file
for i in image_urls:
    res = requests.get(i, stream=True)

    file_name = image_names[counter].replace('.', '')
    file_name = file_name.replace('?', '')
    file_name = file_name + ".jpg"

    # Full path to save the original image
    full_path = os.path.join(folder_path, file_name)

    if res.status_code == 200:
        with open(full_path, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image successfully Downloaded: ', file_name)

        # open downloaded image, resize it and overwrite original
        original_image = Image.open(full_path)
        new_size = (64, 64)
        resized_image = original_image.resize(new_size)
        resized_image.save(full_path)

    else:
        print('Image could not be retrieved.')

    counter += 1
