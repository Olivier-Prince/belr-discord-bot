#! /bin/bash
docker start mongo
# Virtual env creation
# Comment line if already exist
#python -m venv venv
# Virtual env creation & activation
#source venv/bin/activate
# Dependancies
#python -m pip install --upgrade pip wheel setuptools
#python -m pip install -r requirements.txt
# MongoDB creation
cd database && python create_db.py
#python -m database.create_db
# Topic classifier training
cd ../models && python create_topic_classifier.py
# Run the bot
cd .. && python -m bot.app
