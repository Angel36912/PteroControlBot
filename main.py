import discord 
from discord.ext import commands
from parsingdata import config


class Bot:
        def __init__(self):
                self.token = config['token']

                