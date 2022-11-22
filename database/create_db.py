#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @IDE         PyCharm
# @Project     belr-discord-chatbot
# @Filename    create_db.py
# @Directory
# @Author      belr
# @Date        19/11/2022
"""
Create MongoDB with posts from stackexchange on multiple topics like :
Astronomy, Space, Electronic, Engineering, ...
Knowledge of the BOT
"""
# -----------------------------------------------------------------------------
# Copyright (c) 2015, the IPython Development Team and José Fonseca.
#
# Distributed under the terms of the Creative Commons License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#
#
# REFERENCES:
# http://ipython.org/ipython-doc/rel-0.13.2/development/coding_guide.html
# https://www.python.org/dev/peps/pep-0008/
# -----------------------------------------------------------------------------
'''
OPTIONS -----------------------------------------------------------------------
A description of each option that can be passed to this script
ARGUMENTS ---------------------------------------------------------------------
A description of each argument that can or must be passed to this script
'''
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# stdlib imports --------------------------------------------------------------
import os
import json
import decouple
import html2markdown
import xml.etree.ElementTree as ET

# Third-party imports ---------------------------------------------------------
from pymongo import MongoClient

# Our own imports -------------------------------------------------------------

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
# MongoDB configuration
DB_NAME = decouple.config('DB_NAME')
DB_HOST = decouple.config('DB_HOST')
DB_USER = decouple.config('DB_USER')
DB_PASSWD = decouple.config('DB_PASSWD')
URI = "mongodb://%s:%s@%s:27017" % (DB_USER, DB_PASSWD, DB_HOST)
# CLOUD_URI = "mongodb+srv://olivier:olivier@starkbot-cluster.y0aps.mongodb.net/\
# StarkBotBD_Atlas?retryWrites=true&w=majority"

# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------
try:
    connection = MongoClient(URI)
    # connection = MongoClient(CLOUD_URI)

    # STARKBOT DB creation
    db = connection[DB_NAME]
    # QUEST_REP collection creation in StarkBotDB
    collection_Quest_Rep = db.Quest_Rep
    # SUGGESTION collection creation in StarkBotDB
    collection_Suggestion = db.Suggestion
    # EMOTION collection creation in StarkBotDB
    collection_Emotion = db.Emotion
    # RATING collection creation in StarkBotDB
    collection_Rating = db.Rating

except MongoClient.DoesNotExist:
    print("\n" + "=" * 80 + "\n")
    print("⚠️  Could NOT connect to Mongo server")
    print("\n" + "=" * 80 + "\n")


data_path = "stackexchange"
# subdir = "workplace.meta.stackexchange.com"
file_name_pattern = "Posts.xml"

# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
def add_posts(data, language, topic, ident=1, old_ident=1):
    posts = []
    for i in range(len(data['conversations'])):
        for j in range(2):
            if j == 0:
                PostTypeId = 1
                post = {
                    'Id': ident,
                    'PostTypeId': str(PostTypeId),
                    'Score': '1',
                    "ViewCount": "1",
                    'Title': data['conversations'][i][j],
                    "AnswerCount": "1",
                    'Language': language,
                    'Topic': topic,
                }
            else:
                PostTypeId = 2
                post = {
                    'Id': ident,
                    'PostTypeId': str(PostTypeId),
                    'ParentId': str(old_ident),
                    'Score': '1',
                    'Body': data['conversations'][i][j],
                    'Language': language,
                    'Topic': topic,
                }
            posts.append(post)
            old_ident = ident
            ident += 1
    return posts, ident, old_ident


def create_mongodb_database(src, file_name):
    """
    Create mongoDB using all "Posts.xml" files in SUBDIR of SRC
    """
    # os.path.join(data_path, file)
    ident = 1
    old_ident = 1
    posts_list = []

    # INITIAL posts COUNT in DB
    init_present_posts = collection_Quest_Rep.count_documents({})
    print(init_present_posts, "posts are stored in", db.name)

    # Scan subdir SRC or DATA_PATH
    # Make sure that json OR xml files are present
    for subdir in os.listdir(src):
        current_path = os.path.join(src, subdir)
        print(str.upper(current_path), "upload to MongoDB in progress ...")

        # Scan files in SUBDIR
        for file in os.listdir(current_path):

            # Posts.xml load into DB
            if file == file_name:
                filename = os.path.join(current_path, file)
                xml_handle = open(filename, 'r')
                posts_tree = ET.parse(xml_handle)
                posts = posts_tree.getroot()

                # TOPIC preprocessing depending on subdir is suffixed META
                topic = subdir
                # if "meta" in subdir:
                #     topic = subdir[:-23]
                #     # print(topic)
                # else:
                #     topic = subdir[:-17]

                # Posts from "Posts.xml" stored in posts_list
                posts_list = [row.attrib for row in posts]

                for post in posts_list:
                    # Text preprocessing
                    post['Body'] = html2markdown.convert(post['Body'])
                    post['Topic'] = topic
                    post['Language'] = 'english'

                    # TEST on Id AND Topic
                    query = collection_Quest_Rep.count_documents({
                        "$and": [{
                            "Id": post["Id"],
                            "Topic": post["Topic"]}]})

                    # After test IF NOT PRESENT
                    # Test post is Answer or Question with Answer
                    # Post INSERTION in Quest_Rep collection
                    if (query == 0) and (
                            (post["PostTypeId"] == '2') or (
                            (post["PostTypeId"] == '1') and
                            (post['AnswerCount'] is not None))):
                        collection_Quest_Rep.insert_one(post)
                        # print("Post", post["_id"], "inserted")

            if file == "my_export_en.json":
                curent_file = os.path.join(current_path, file)
                with open(curent_file) as f:
                    data = json.load(f)
                topic = 'general'
                language = 'english'
                posts, ident, old_ident = add_posts(data,
                                                    language,
                                                    topic,
                                                    ident + 1,
                                                    old_ident + 1)
                collection_Quest_Rep.insert_many(posts)

    # INSERTED posts COUNT in DB
    present_posts = collection_Quest_Rep.count_documents({})
    inserted_posts = present_posts - init_present_posts
    print(inserted_posts, "posts have been inserted in", db.name)
    print(present_posts, "posts are stored in", db.name)

    # Create ID index
    db.Quest_Rep.create_index("Id")

    # Create POST_TYPE_ID index
    db.Quest_Rep.create_index("PostTypeId")

    # Create TOPIC index
    db.Quest_Rep.create_index("Topic")

    # Create SCORE index
    db.Quest_Rep.create_index("Score")

    # Create PARENTID index
    db.Quest_Rep.create_index("ParentId")

    # Create ANSWERCOUNT index
    db.Quest_Rep.create_index("AnswerCount")

    # Create TEXT_SEARCH index
    db.Quest_Rep.create_index([('Title', 'text'), ('Body', 'text')],
                              weights={'Title': 2, 'Body': 1},
                              name="text_search")

    # QUEST_REP collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Quest_Rep)
    # SUGGESTION collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Suggestion)
    # EMOTION collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Emotion)
    # RATING collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Rating)

    return posts_list


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 80 + "\n")
    print("create_db is running ...")
    create_mongodb_database(data_path, file_name_pattern)
    print("\n" + "=" * 80 + "\n")
