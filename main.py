import os
import discord
from discord.ext import commands
from collections import defaultdict

# Client Instance: All commands will start with '.'
client = commands.Bot(command_prefix='.')


# Class Definitions
class FrequencyMap:
    def __init__(self, name):
        self.name = name
        self.wordFreq = defaultdict(int)
        self.sortedKeys = None


############################
# Word Frequency Functions #
############################


#
# Generate Word Frequency
#
# Take each word in the input and count up it's occurances
#
def generateWordFrequency(author, userInput):
    # defaultdict(int): If a key doesn't exist, add it with a default value of 0
    wordFreq = author.wordFreq
    for word in userInput.casefold().split():
        wordFreq[word] += 1

    # sorted() returns a *list* of key from most freq keys to least freq keys
    sorted_wordFreqKeys = sorted(wordFreq, key=wordFreq.get, reverse=True)

    return author, wordFreq, sorted_wordFreqKeys


#
# Print Word Frequency
#
def printWordFreq(user):
    print(f'     [Word Count for {user.name}]')
    for currentKey in user.sortedKeys:
        print(f"     {currentKey}: {user.wordFreq[currentKey]}")

    return


#
# Word Frequency String
#
def createWordFreqString(user):
    word_frequency = f'[Word Count for {user.name}]\n'
    for currentKey in user.sortedKeys:
        word_frequency += (f"     {currentKey}: {user.wordFreq[currentKey]}\n")

    return word_frequency


##########
# Events #
##########


# On Ready Event
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


# TODO: Change to db[] eventually
users = dict()


# NOTE: functions decorated with @client.listen recieves 'Message' instances
# Listen for Messages (Recieves message object)
# All events will be slow because this function is ran first?
@client.listen('on_message')
async def on_message(message):
    # Prevents bot from responding to itself
    if message.author == client.user:
        return

    # Look up author_freq_map of message
    if message.author in users:
        # Existing User: Pull up from database
        author_freq_map = users[message.author]
    else:
        # New User: Add to database
        author_freq_map = FrequencyMap(message.author)
        users.update({message.author: author_freq_map})

    # Create a word frequency map based on the recieved message
    word_frequency = generateWordFrequency(author_freq_map, message.content)

    # Update the author_freq_map's word frequency table
    author_freq_map = word_frequency[0]
    author_freq_map.wordFreq = word_frequency[1]
    author_freq_map.sortedKeys = word_frequency[2]

    # DEBUG: Prints frequency map to CONSOLE
    # printWordFreq(author_freq_map)
    # print('\n')

    # DEBUG:
    # message.author: MafuMafu Tofu
    # message.author.name: MafuMafu Tofu
    # message.author.display_name/.nick = Tim
    # print(f'  {message.author}: {message.content}')


############
# Commands #
############

# NOTE: functions decorated with @client.command recieves 'Context' instances


# Test Mention
@client.command()
async def mention(ctx, mentioned_user : discord.Member):
    await ctx.send(f'{mentioned_user}')


# Test Mention
@client.command()
async def test(ctx):
    test = ctx.author
    await ctx.send(f'{test}')


@client.command()
async def eli(ctx):
    await ctx.send('Eli? She\'s only the cutest girlfriend around!')


# NOTE: name_of_variable : type_of_instance is discord.py conversion
@client.command()
async def freq(ctx, mentioned_user : discord.Member):
    # If no mention was included in the mention, return.
    # if len(ctx.message.mentions) < 1:
    #     return

    if mentioned_user in users:
        # printWordFreq(users[mentioned_user])
        word_frequncy_string = createWordFreqString(users[mentioned_user])
        await ctx.send(word_frequncy_string)

# TODO: Look up type() vs isinstance()
# Error handiling specific to freq() command
@freq.error
async def freq_error(ctx, error):
    # isinstance(incoming_instance, is_instance_this_type)
    if isinstance(error, commands.MissingRequiredArgument):
        print(f'ERROR: {ctx.author} did not specify which member to look up.')


# Run the Client
client.run(os.getenv('TOKEN'))
