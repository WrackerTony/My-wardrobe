import os
import json
from os.path import join, exists
from kivy.utils import platform

# Determine the base directory for saving tags

base_dir = os.path.dirname(__file__)

data_dir = join(base_dir, "data")

# Ensure the directory exists
if not exists(data_dir):
    os.makedirs(data_dir)

tags_file = join(data_dir, "photo_tags.json")

def load_tags():
    if not exists(tags_file):
        return {}
    with open(tags_file, "r") as f:
        return json.load(f)

def save_tags(tags):
    with open(tags_file, "w") as f:
        json.dump(tags, f, indent=4)

def add_tag(photo_id, tag):
    tags = load_tags()
    if photo_id not in tags:
        tags[photo_id] = []

    if "," in tag:
        tag_list = tag.split(",")
        for t in tag_list:
            t = t.strip()
            if t and t != "Select type" and t not in tags[photo_id]:
                tags[photo_id].append(t)
    else:
        tag = tag.strip()
        if tag and tag != "Select type" and tag not in tags[photo_id]:
            tags[photo_id].append(tag)
    
    save_tags(tags)

def get_tags(photo_id):
    tags = load_tags()
    return tags.get(photo_id, [])

def search_tags(tag_list):
    tag_list = [tag.strip() for tag in ",".join(tag_list).split(",") if tag.strip() and tag != "Select Item"]
    photos_with_the_tags = []
    tags_data = load_tags()
    if not tags_data:
        return photos_with_the_tags

    for photo_id, tags in tags_data.items():
        if all(tag in tags for tag in tag_list):
            photos_with_the_tags.append(photo_id)
    
    return photos_with_the_tags

def delete_tags(photo_id):
    tags = load_tags()
    if photo_id in tags:
        del tags[photo_id]
        save_tags(tags)
        print("Tags deleted.")
    else:
        print("Failed to delete tags.")