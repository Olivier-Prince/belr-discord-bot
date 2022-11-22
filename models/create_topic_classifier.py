#!/user/bin/env python3 -tt
# -*- coding: utf-8 -*-
# @IDE:         PyCharm
# @Project:     discord-smartbot
# @Filename:    create_topic_classifier.py
# @Directory:   models
# @Author:      belr
# @Time:        21/11/2022
"""A one-line description or name.

A longer description that spans multiple lines.  Explain the purpose of the
file and provide a short list of the key classes/functions it contains.  This
is the docstring shown when some does 'import foo;foo?' in IPython, so it
should be reasonably useful and informative.
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
from time import time

# Third-party imports ---------------------------------------------------------
import pickle
import decouple
import numpy as np
import pandas as pd

from pymongo import MongoClient

from nltk.corpus import stopwords as sw

from sklearn.preprocessing import LabelEncoder

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import ShuffleSplit

from collections import defaultdict
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfTransformer

# Our own imports -------------------------------------------------------------
# from database.create_db import *

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------
topic_max_questions = 5000
file_name = "topic_classifier.pickle"

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
DB_NAME = decouple.config('DB_NAME')
DB_HOST = decouple.config('DB_HOST')
DB_USER = decouple.config('DB_USER')
DB_PASSWD = decouple.config('DB_PASSWD')
URI = "mongodb://%s:%s@%s:27017" % (DB_USER, DB_PASSWD, DB_HOST)

# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------
# nltk.download('stopwords')

stopwords = sw.words('english')

pipe0 = Pipeline([
    ("ngram_stop", CountVectorizer(
        stop_words=stopwords, ngram_range=(1,2), min_df=2
    )),
    ('tfidf', TfidfTransformer()),
    ('sgd-weight_bal', SGDClassifier(
        max_iter=2000, class_weight='balanced',
        penalty='elasticnet', loss='modified_huber'
    )),
])

# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
def run_pipes(pipes, splits, corpus, target, test_size=0.2, seed=42):
    res = defaultdict(list)
    spliter = ShuffleSplit(n_splits=splits, test_size=test_size, random_state=seed)

    for idx_train, idx_test in spliter.split(corpus, target):

        for pipe in pipes:
            # Name of the model
            name = "-".join([x[0] for x in pipe.steps])

            # Split datasets
            X_train = corpus[idx_train]
            X_test = corpus[idx_test]
            y_train = target[idx_train]
            y_test = target[idx_test]

            # Train
            start = time()
            pipe.fit(X_train, y_train)
            fit_time = time() - start

            # Test & save results
            y = pipe.predict(X_test)
            res[name].append([
                fit_time,
                f1_score(y_test, y, average='micro'),
                f1_score(y_test, y, average='macro'),
                f1_score(y_test, y, average='weighted'),
            ])
    return res


def print_table(result):
    # Compute mean & std
    final = {}
    for model in result:
        arr = np.array(result[model])
        final[model] = {
            "time (s)": arr[:, 0].mean().round(2),
            "f1_av_micro": [arr[:, 1].mean().round(3), arr[:, 1].std().round(3)],
            "f1_av_macro": [arr[:, 2].mean().round(3), arr[:, 2].std().round(3)],
            "f1_av_weighted": [arr[:, 3].mean().round(3), arr[:, 3].std().round(3)],
        }

    df = pd.DataFrame.from_dict(final, orient="index").round(3)
    return df


def main(filename):
    """
    Create topic classifier
    """
    client = MongoClient(URI)

    db = client[DB_NAME]
    collection = db['Quest_Rep']
    collection.index_information()

    topics = collection.distinct('Topic')
    nb_topics = len(topics)

    label_encoder = LabelEncoder()
    label_encoder.fit(topics)

    corpus = []
    target = []

    for topic in topics:

        query = {"Topic": topic, "PostTypeId": "1"}

        if collection.count_documents(query) >= topic_max_questions:

            questions = collection.find(query).sort([('Score', -1)]).limit(topic_max_questions)

            corpus.extend([question.get("Title") for question in questions])
            target.extend([topic] * topic_max_questions)

        else:
            length = collection.count_documents(query)

            questions = collection.find(query).sort([('Score', -1)]).limit(length)

            corpus.extend([question.get("Title") for question in questions])
            target.extend([topic] * length)

    corpus = np.array(corpus)
    target = np.array(target)

    # Topics size
    for topic in topics:
        query = {"Topic": topic, "PostTypeId": "1"}
        topic_size = collection.count_documents(query)
        print("Posts", str.upper(topic), "\n\t\t\t", topic_size)

    # encode targets (str) to numerical (int)
    y = label_encoder.transform(target)

    vectorizer = CountVectorizer(stop_words=stopwords)
    X = vectorizer.fit_transform(corpus)

    result = run_pipes([pipe0], splits=10, corpus=corpus, target=y)
    pickle.dump(pipe0, open(filename, 'wb'))

    print("\nRESULTS :\n")

    return result


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print("\ncreate_topic_classifier is running ...\n")
    with pd.option_context('display.max_columns', None):
        print(print_table(main(file_name)))
    print("\nTOPIC classifier saved to file", file_name)
    print("\n" + "=" * 80 + "\n")
