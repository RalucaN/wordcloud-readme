from wordcloud import WordCloud
from bs4 import BeautifulSoup
import string
import re
from PIL import Image
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

readme_path = config['DEFAULT']['readme_path']
mask_file = config['DEFAULT']['mask_file']
width = int(config['DEFAULT']['width'])
height = int(config['DEFAULT']['height'])
background_color = config['DEFAULT']['background_color']
contour_color = config['DEFAULT']['contour_color']
contour_width = int(config['DEFAULT']['contour_width'])
collocations = config['DEFAULT'].getboolean('collocations')
use_mask = config['DEFAULT'].getboolean('use_mask')
wordcloud_output = config['DEFAULT']['wordcloud_output']

stop_words = set(config['EXCLUSIONS']['stop_words'].split(', '))
excluded_words = set(config['EXCLUSIONS']['excluded_words'].split(', '))

def read_readme():
    with open(readme_path, 'r', encoding='utf-8') as readme_file:
        return readme_file.read()

def extract_text_from_markdown(markdown_content):
    soup = BeautifulSoup(markdown_content, 'html.parser')
    cleaned_text = ' '.join(soup.stripped_strings)
    
    cleaned_text = re.sub(r'http\S+|www.\S+', '', cleaned_text, flags=re.MULTILINE)
    
    words = cleaned_text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    filtered_words = [word for word in filtered_words if word.lower() not in excluded_words]

    filtered_words = [''.join(c for c in w if c not in string.punctuation) for w in filtered_words]
    filtered_words = [word for word in filtered_words if word]

    return ' '.join(filtered_words)

markdown_content = read_readme()
cleaned_content = extract_text_from_markdown(markdown_content)

if use_mask:
    bubble_mask = np.array(Image.open(mask_file))
    wordcloud = WordCloud(width=width, height=height, background_color=background_color, contour_color=contour_color, contour_width=contour_width, collocations=collocations, mask=bubble_mask).generate(cleaned_content)
else:
    wordcloud = WordCloud(width=width, height=height, background_color=background_color, contour_color=contour_color, contour_width=contour_width, collocations=collocations).generate(cleaned_content)

wordcloud.to_file(wordcloud_output)
