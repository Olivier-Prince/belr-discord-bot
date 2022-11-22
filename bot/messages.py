#!/user/bin/env python3 -tt
# -*- coding: utf-8 -*-
# @IDE:         PyCharm
# @Project:     discord-smartbot
# @Filename:    messages.py
# @Directory:   bot
# @Author:      belr
# @Time:        19/11/2022
"""Messgaes to be displayed in Discord channel."""
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

# Third-party imports ---------------------------------------------------------
import decouple

# Our own imports -------------------------------------------------------------

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
BOT_NAME = decouple.config('BOT_NAME')


# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------
# WELCOME message (64 pix/line)
welcome_message = "```   __,_,\n  [_|_/           Hello\n   //\n _//    __            My name is %s\n(_|)   |@@|\n \ \__ \--/ __            Initialy created by the Stark Agency @ SIMPLON.co\n  \o__|----|  |   __\n      \ }{ /\ )_ / _\              Now maintained by BelR\n      /\__/\ \__O (__\n     (--/\--)    \__/\n     _)(  )(_                                        ID: CAABMBJMOPLR\n    `---''---`\n```" % str(BOT_NAME)

# AUTO message (64 pix/line)
auto_message = "```css\nI would be pleased to help you on this topics :\n  - 🚀 Space\n  - 🌠 Astronomy\n  - 🤓 Engineering\n  - 📊 Datascience\n  - 🌍 Earthscience\n\nFor more information you may type : '\help'\n\nInitialy created by the Stark Agency during an amazing BOT DEV contest @ SIMPLON.co !\nNow maintained by BelR @ https://github.com/belr20/discord-smartbot\n\nHave a nice day 🌞```"

# TEST message (64 pix/line)
test_message = "```  __,_,\n  [_|_/           Hello,\n   //\n _//    __             I am here at your service 🙏\n(_|)   |@@|\n \ \__ \--/ __             TheDoctor-SmartBot 🤖\n  \O__| }{ |  |   __\n      \    /\ )_ / _\            On BelR Discord server\n      /\__/\ \__O (__\n     (  /\  )    \__/\n     _)(  )(_                            ID : CAABMBJMOPLR           \n    `---''---`\n```"

# HELP message (64 pix/line)
help_message = "```css\nHello %s,\n\nMy name is %s, I am a cool & smart BOT maintained by BelR from SIMPLON.co\n\nActually, I am an expert in :\n  - 🚀 Space\n  - 🌠 Astronomy\n  - 🤓 Engineering\n  - 📊 Datascience\n  - 🌍 Earthscience\nYou can ask me anything on this topics 👌\n\nBy prefixing with \, you can also use the commands bellow :\n\mute       => 🔇 when i am too chatty\n\\unmute     => 🔊 to (re)activate\n\suggestion => 💡 to make a suggestion\n\ping       => 🔗 to be sure I am with you\n\date       => 📅 what is the day today ?\n\\bonjour    => 😁 for a smile\n\emotion    => 🔮 to predict your daily mood\n\imp        => 'Id' 'Topic' your message\n\nYou may also check the documentation @ https://github.com/belr20/discord-smartbot```"

# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
