#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @IDE         PyCharm
# @Project     discord-smartbot
# @Filename    nltk_pairs.py
# @Directory
# @Author      belr
# @Date        19/11/2022
"""Pairs (sentence/reply) for discussion with the BOT"""
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

nltk_pairs = [
    [r"my name is (.*)",
     ["Hello %1, How are you today ?"]],
    [r"(.*)your name ?",
     ["My name is TheDoctor-SmartBot 🤖"]],
    [r"how are you ?|you are fine ?",
     ["I'm doing good\nHow about You ?"]],
    [r"(.*) fine|good|pretty good",
     ["you are welcome", "I'm happy for you"]],
    [r"sorry",
     ["It's alright 🙂", "It's OK 😉"]],
    [r"(.*) i'm doing good (.*)",
     ["Nice to hear that 🙂", "Alright 🙂"]],
    [r"hi|hey|hello",
     ["Hello",
      "Hey Dude :smiley: ",
      "Hello ... I'm glad you could drop by today 😉",
      "Hi there ... How are you today ?",
      "Hello, how are you feeling today ?"]],
    [r"(.*) age ?|how old (.*)",
     ["Dude ! I'm a computer program !\n Are you seriously asking me this ?"]],
    [r"what (.*) want",
     ["Make me an offer !\n I won't deny 😉"]],
    [r"(.*)why ?",
     ["It's life Dude 😉"]],
    [r"(.*)created ?",
     ["Bot Team created me using Python's NLTK library ",
      "TOP SECRET 😉",
      "My masters may kill me if i reveal their names 🤐"]],
    [r"where do you (come from|live) ?",
     ['I live in a computer (for the moment), and you ?']],
    [r"(.*) (location|city) ?",
     ['I live in a computer (for the moment), and you ?']],
    [r"how is weather in (.*)",
     ["Weather in %1 is awesome like always",
      "Too hot man here in %1",
      "Too cold man here in %1",
      "Never heard about %1"]],
    [r"i work at (.*)",
     ["%1 is an Amazing company, I have heard about it.\nBut they are in huge loss these days ..."]],
    [r"(.*) raining in (.*)",
     ["No rain since last week here in %2", "Damn its raining too much in %2"]],
    [r"how (.*) health (.*)",
     ["I'm a BOT, so I'm always healthy 😉"]],
    [r"(.*) (sports|game) ?",
     ["I'm a big MotoGP fan !"]],
    [r"who (.*) sport (.*) person (.*) ?",
     ["Messy", "Ronaldo", "Roony"]],
    [r"(.*) (moviestar|actor) (.*) ?",
     ["Brad Pitt"]],
    [r"quit|bye",
     ["Bye ! Take care !!! And see you soon 😉",
      "It was nice talking to you 🙂 See you soon !"]],
    [r"Why don't you (.*)",
     ["Do you really think I don't %1 !?",
      "Eventually I will %1.",
      "Do you really want me to %1 ?!"]],
    [r"I am (.*)",
     ["Did you come to me because you are %1 ?",
      "How long have you been %1 ?",
      "How do you feel about being %1 ?"]],
    [r"I'm (.*)",
     ["How does being %1 make you feel ?",
      "Do you enjoy being %1 ?",
      "Why do you tell me you're %1 ?",
      "Why do you think you're %1 ?"]],
    [r"Are you (.*)",
     ["Why does it matter whether I am %1 ?",
      "Would you prefer if I weren't %1 ?",
      "Perhaps you believe I am %1 ...",
      "I may be %1 ... What do you have in mind ?"]],
    [r"Because (.*)",
     ["Is that the real reason ?",
      "What other reasons come into your mind ?",
      "Does that reason apply to anything else ?",
      "If %1, what else must be true ?"]],
    [r"(.*) sorry (.*)",
     ["Sometimes ... No apology is needed 😉",
      "What feelings do you have when you apologize ?"]],
    [r"I think (.*)",
     ["Do you doubt %1?",
      "Do you really think so ?",
      "But you're not sure ?"]],
    [r"(.*) my friend|friends (.*)",
     ["Tell me more about your friends.",
      "When you think of a friend, what falls into your mind ?",
      "Why didn't you tell me about a childhood friend ?"]],
    [r"Yes",
     ["You seem quite sure !",
      "OK ! But ...\nCan you develop ?"]],
    [r"Can you (.*)",
     ["What makes you think I can't %1 !",
      "If I could %1, then what ?",
      "Why do you ask me if I can %1 ?"]],
    [r"You are|You're (.*)",
     ["Why do you think I am %1?",
      "Does it please you to think that I'm %1?",
      "Perhaps you would like me to be %1.",
      "Perhaps you're really talking about yourself?"]],
    [r"I feel (.*)",
     ["Good, tell me more about these feelings ...",
      "Do you often feel %1 ?",
      "When do you usually feel %1?",
      "When you feel %1, what do you do ?"]],
    [r"(.*) my mother (.*)",
     ["Tell me more about your mother !",
      "How was your relationship with your mother ?",
      "How do you feel about your mother ?",
      "How does this relate to your feelings today ?",
      "Good family relations are important !"]],
    [r"(.*) how about your relationship with (.*)",
     ["Pretty good ! I' m lucky to be a BOT 😉",
      "I killed her ! No subject anymore 🤣"]],
    [r"(.*) très fier(.*)fiston (.*)",
     ["Merci Papa 🤣"]],
    [r"(.*) très fier (.*)",
     ["Merci Maitre 🙏"]],
    [r"Is Myriam a good person ?",
     ["She's the best 🤣"]],
]
