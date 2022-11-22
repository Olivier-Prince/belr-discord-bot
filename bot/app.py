#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @IDE         PyCharm
# @Project     belr-discord-chatbot
# @Filename    app.py
# @Directory   bot
# @Author      belr
# @Date        19/11/2022
"""Run the BOT"""
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
import re
import asyncio
import datetime

# Third-party imports ---------------------------------------------------------
import pickle
import discord
import decouple
import numpy as np

from chatterbot import ChatBot
from nltk.chat.util import Chat, reflections
from sklearn.preprocessing import LabelEncoder
from chatterbot.trainers import ChatterBotCorpusTrainer

# Our own imports -------------------------------------------------------------
from bot.messages import (welcome_message, auto_message, help_message,
                          test_message, BOT_NAME)
from database.create_db import (db, collection_Quest_Rep, collection_Rating,
                                collection_Suggestion, collection_Emotion)
from bot.nltk_pairs import nltk_pairs

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
# Channel ID for the BOT
TOKEN = decouple.config('TOKEN')
DISCORD_CHANNEL = int(decouple.config('DISCORD_CHANNEL'))

# TIMEOUT for auto message on start-up & every 60 minutes
TIMEOUT = 60 * 60

# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------
# Today date
date = datetime.datetime.now()

# TOPIC classifier load
filename: str = 'models/topic_classifier.pickle'
classif_topic = pickle.load(open(filename, 'rb'))

# EMOTION classifier load
filename: str = 'models/emotion.sav'
emotion = pickle.load(open(filename, 'rb'))

# topics = ['astronomy', 'datascience', 'earthscience', 'engineering',
#           'general', 'space', 'stellar']
topics = collection_Quest_Rep.distinct('Topic')
nb_topics = len(topics)

label_encoder_topic = LabelEncoder()
label_encoder_topic.fit(topics)


# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------
class Bot(discord.Client, Chat):

    def __init__(self, pairs, nltk_reflections, flag=True):
        """
        Bot class inherits from discord.Cliend and nltk.Chat
        """
        discord.Client.__init__(self, intents=discord.Intents.all())
        Chat.__init__(self, pairs, nltk_reflections)
        self.flag = flag
        self.flag = True
        self.chatterbot = self.chatterbot_respond('thedoctor-smartbot')

    def nltk_respond(self, message):
        """
        NLTK chatBot
        """
        return self.respond(str(message))

    def chatterbot_respond(self, name):
        """
        Chatterbot
        """
        chatbot = ChatBot(
            name,
            # storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
            logic_adapters=[
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.BestMatch'
            ],
            # database_uri=str(URI + "/" + DB_NAME)
        )
        trainer = ChatterBotCorpusTrainer(chatbot)
        # TRAIN Corpus
        trainer.train("chatterbot.corpus.english")
        return chatbot

    async def on_ready(self):
        print("\n" + "=" * 80 + "\n")
        print('BOT is logged in as :')
        print('\tName\n\t\t\t', self.user.name)
        print('\tID\n\t\t\t', self.user.id)
        print('On Discord channel')
        print("\tID\n\t\t\t", DISCORD_CHANNEL)
        print("Connected to Mongo server")
        print(f"\tHost\n\t\t\t{db.client.HOST}:{db.client.PORT}")
        print("\tDB\n\t\t\t", db.name)
        print("\n" + "=" * 80 + "\n")
        print("Available TOPICS :")
        for topic in topics:
            print("\t\t\t", topic)
        print("\n" + "=" * 80 + "\n")
        channel = client.get_channel(DISCORD_CHANNEL)
        await channel.send(welcome_message)
        while True:
            # print("while loop in on_ready")
            await channel.send(auto_message)
            await asyncio.sleep(TIMEOUT)

    async def on_message(self, message):
        # LOWERCASE message
        mess = message.content
        mess = str.lower(mess)

        # Bot do not respond to itself
        if message.author == self.user:
            return
        else:
            # Bot BASIC commands
            if mess.startswith("\\"):
                if mess == "\\unmute":
                    self.flag = True
                    await message.channel.send(
                        'Hey ! Nice to see you again 🙂 How may I help you ?'
                    )

                if mess == "\\mute":
                    self.flag = False
                    await message.channel.send(
                        "Thanks, I was pleased to see you 🙂")
                    msg = await message.channel.send(
                        "```How was your user experience ?```")
                    await msg.add_reaction('😃')
                    await msg.add_reaction('😐')
                    await msg.add_reaction('🙁')

                    reac_list = ['😃', '😐', '🙁']
                    check = lambda reaction, user: user == message.author and str(reaction) in reac_list

                    try:
                        # Waiting for the reaction
                        reaction, user = await client.wait_for(
                            'reaction_add', check=check, timeout=30.0
                        )

                        if str(reaction) == "😃":
                            collection_Rating.insert_one({"rate": 2})
                            await message.channel.send(
                                "```Thank you, I was pleased to help you 🙂```"
                            )

                        if str(reaction) == "😐":
                            collection_Rating.insert_one({"rate": 1})
                            await message.channel.send(
                                "```Thank you, I hope I will do better next time 🙁```"
                            )

                        if str(reaction) == "🙁":
                            collection_Rating.insert_one({"rate": 0})
                            await message.channel.send(
                                "```Thank you, I hope I will do better next time 🙏```"
                            )

                    except asyncio.TimeoutError:
                        await msg.delete()

                if mess == "\\shutdown":
                    await message.channel.send("Bye bye ✌")
                    await self.close()

                if self.flag is True:

                    if mess.startswith("\\suggestion"):

                        request = mess[12:]

                        collection_Suggestion.insert_one({
                            "User": str(message.author),
                            "Suggestion": request})

                        await message.channel.send(
                            "Thank you **%s** for your suggestion : **%s**"
                            % (str(message.author)[:-5],
                               request))

                    if mess.startswith("\\imp"):
                        listmess = mess.split(sep=" ")
                        PID = listmess[1]
                        TOP = listmess[2]
                        BODlist = listmess[3:]
                        BOD = "[NON VERIFIED] %s" % ' '.join(BODlist)
                        collection_Quest_Rep.insert_one({
                            "Topic": TOP,
                            "Body": BOD,
                            "ParentId": PID,
                            "PostTypeId": 2,
                            "Score": 10})
                        await message.channel.send(
                            "Many thanks for this valuable contribution 🙏")

                    if mess == "\\get rating":
                        list_rating = collection_Rating.find()
                        bot_ratings = [resp.get("rate") for resp in list_rating]
                        good = bot_ratings.count(2)
                        medium = bot_ratings.count(1)
                        bad = bot_ratings.count(0)
                        await message.channel.send(
                            "Bot rating  :\n\nGood -> **%s**\nMedium -> **%s**\nBad -> **%s**" % (good, medium, bad)
                        )

                    if mess == "\\get suggestion":
                        list_sugg = collection_Suggestion.find()
                        bot_sugg = [resp.get("Suggestion") for resp in list_sugg]
                        print("BOT suggestion :", bot_sugg)
                        bot_sugg = '    ;   '.join(bot_sugg)
                        with open("result.txt", "w") as file:
                            file.write(bot_sugg)
                        with open("result.txt", "rb") as file:
                            await message.channel.send(
                                "Your file is:",
                                os.remove("result.txt"))

                    if mess == "\\emotion":
                        list_emotion = collection_Emotion.find({
                            "User": str(message.author)})
                        list_feel = [resp.get("Message")
                                     for resp in list_emotion]
                        list_feel = ' '.join(list_feel)
                        list_feel = [list_feel]
                        feel = emotion.predict(list_feel)
                        await message.channel.send(
                            "Hey! Looks like you feel: %s"
                            % feel)

                    if mess == "\\help":
                        await message.channel.send(
                            help_message % (message.author.display_name, BOT_NAME)
                        )

                    if mess == "\\ping":
                        await message.channel.send(
                            "Pong in {:.0f} ms 👌".format(self.latency * 1000)
                        )

                    if mess == "\\date":
                        await message.channel.send("**%s**" % str(date)[:-7])

                    if mess == "\\test":
                        await message.channel.send(test_message)

                    if mess == "\\bonjour":
                        await message.channel.send(
                            "Bonjour **%s** 🤗" % str(
                                message.author.display_name
                            )
                        )

            # BASIC conversation
            else:
                if self.flag is True:
                    # TOPIC identification
                    topic = classif_topic.predict([mess])
                    topic = label_encoder_topic.inverse_transform(topic)
                    print(str.upper(topic[0]), "topic has been detected.")
                    liste_posible_values = list(range(nb_topics))
                    liste_topic = list(label_encoder_topic.inverse_transform(liste_posible_values))
                    pred_proba = classif_topic.predict_proba([mess])
                    liste_proba = list(pred_proba[0])

                    # NLTK chatBot
                    flag_resp = False
                    resp = self.nltk_respond(mess)
                    if resp:
                        flag_resp = True
                        collection_Emotion.insert_one({
                            "User": str(message.author),
                            "Message": mess,
                            "Date": str(date)[:-7]})
                        await message.channel.send(resp)

                    # Chatterbot
                    if (topic[0] == 'general') and (flag_resp is False):
                        flag_resp = True
                        mess_chatterbot = mess.upper()

                        collection_Emotion.insert_one({
                            "User": str(message.author),
                            "Message": mess,
                            "Date": str(date)[:-7]})

                        resp = self.chatterbot.get_response(mess_chatterbot)
                        await message.channel.send(resp)

                    # MongoDB Query
                    if flag_resp is False:
                        if topic[0] != 'general':
                            for i in range(nb_topics):
                                best_topic = liste_topic[np.argmax(liste_proba)]
                                msg = await message.channel.send(
                                    "Are you looking for information about %s ?\nWould you please confirm by yes or no" % best_topic
                                )
                                await msg.add_reaction('✅')
                                await msg.add_reaction('❌')
                                reac_list = ['✅', '❌']
                                check = lambda reaction, user: user == message.author and str(reaction) in reac_list
                                try:
                                    # Waiting for the reaction
                                    reaction, user = await client.wait_for(
                                        'reaction_add',
                                        check=check,
                                        timeout=30.0)
                                    if str(reaction) == "✅":
                                        print("Topic AGREEMENT by USER")
                                        break
                                    if str(reaction) == "❌":
                                        print("Topic DISAGREEMENT by USER")
                                        idx = np.argmax(liste_proba)
                                        liste_proba.pop(idx)
                                        liste_topic.pop(idx)

                                except asyncio.TimeoutError:
                                    print("User TOPIC reaction TIMEOUT")
                        else:
                            best_topic = topic[0]

                        try:
                            waiting_gif = await message.channel.send(
                                file=discord.File('assets/images/wait.gif'))
                            resp, quest_id = mongodb_request(
                                mess,
                                best_topic
                            )
                            await waiting_gif.delete()

                            for i in resp:
                                if len(i) > 1900:
                                    i1 = i[:1900]
                                    i2 = i[1901:]
                                    await message.channel.send(i1)
                                    await message.channel.send(i2)
                                else:
                                    await message.channel.send(i)

                                msg = await message.channel.send(
                                    "```Can you help me to improve by rating the relevance of the answer```"
                                )
                                await msg.add_reaction('👍')
                                await msg.add_reaction('👎')

                                reac_list = ['👍', '👎']
                                check = lambda reaction, user: user == message.author and str(reaction) in reac_list

                                try:
                                    # Waiting for the reaction
                                    reaction, user = await client.wait_for('reaction_add', check=check, timeout=60.0)

                                    if str(reaction) == "👍":
                                        await message.channel.send(
                                            "Thanks for your feedback 🙏\nIf I was a human I would be the HAPPIEST 😇")
                                        break

                                    if str(reaction) == "👎":
                                        await message.channel.send(
                                            "```Thank you for your feedback 🙏\nCan you help me to become better with adding an anwser by typing : \\imp %s %s ANSWER```" % (quest_id, best_topic))

                                except asyncio.TimeoutError:
                                    await msg.delete()
                                    break

                        except IndexError:
                            await waiting_gif.delete()
                            resp = "I'm still learning Dude ... \
                            \nWhat do you mean by **%s** ?" % mess
                            await message.channel.send("%s" % resp)


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
def mongodb_request(message, topic):
    """
    Query MongoDB
    """
    title = collection_Quest_Rep.find(
        {"$text": {"$search": message},
         'Topic': topic,
         'AnswerCount': {"$ne": "0"}},
        {'score': {'$meta': 'textScore'}})
    title.sort([('score', {'$meta': 'textScore'})]).limit(1)

    ParentId = title[0].get("Id")
    if isinstance(ParentId, int):
        ParentId = str(ParentId)

    all_resp = collection_Quest_Rep.find({
        'Topic': topic,
        "ParentId": ParentId}).sort([('Score', -1)]).limit(5)
    list_resp = [resp.get("Body") for resp in all_resp]

    final_resp = []
    for i in list_resp:
        i = re.sub('<[^<]+?>', '', i)
        final_resp.append(i)

    return final_resp, ParentId


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    client = Bot(nltk_pairs, reflections)
    client.run(TOKEN)
