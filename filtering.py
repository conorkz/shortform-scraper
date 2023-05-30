import re
import itertools
import os
roi = 'no info on the website'
directory = 'YOUR_DIRECTORY'
with open('data.txt', 'r') as f: # I saved api data in a txt file
    data = f.read()
links = []
for s in re.findall(r'(?<="url_slug":")[^"]+', data):
    links.append(f'https://www.shortform.com/app/book/{s}')
authors = re.findall(r'(?<="author":")[^"]+', data)
amazons = re.findall(r'(?<="amazon_link":")[^"]+', data)
descs = []
for s in re.findall(r'(?<="blurb":")[^"]+', data):
    if s.endswith('\\'):
        s += '\\'  # Add an extra backslash to avoid the error
    descs.append(re.sub('<[^<]+?>', '', s).encode().decode('unicode_escape'))
covers = []
for g in re.findall(r'(?<="cover_image":")[^"]+', data):
    covers.append(g.replace('//',''))
publisheds = re.findall(r'(?<="created":")[^"]+', data)
popularityrs = re.findall(r'"popularity_read_count":(\d+)', data)
tags = re.findall(r'"tags":\[(.*?)\]', data)[:-1]
titles = re.findall(r'(?<="title":")[^"]+', data)
popularityus = re.findall(r'"popularity_user_count":(\d+)', data)
for link, author, amazon, desc, cover, published, popularityr, tag, title, popularityu in itertools.zip_longest(links, authors, amazons, descs, covers, publisheds, popularityrs, tags, titles, popularityus, fillvalue=roi):
    bf = re.sub(r"[^\w\s]", "", title)
    file_name = os.path.join(directory, f"{bf}.txt")
    suffix = 1
    while os.path.exists(file_name):
        file_name = os.path.join(directory, f"{bf} ({suffix}).txt")
        suffix += 1
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Link: {link}\n")
        file.write(f"Title: {title}\n")
        file.write(f"Author: {author}\n")
        file.write(f"Amazon link: {amazon}\n")
        file.write(f"Book cover: {cover}\n")
        file.write(f"Published on: {published}\n")
        file.write(f"Genres: {tag}\n")
        file.write(f"Popularity_read_count: {popularityr}\n")
        file.write(f"Popularity_user_count: {popularityu}\n")
        file.write(f"Description: {desc}\n")