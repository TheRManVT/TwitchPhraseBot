import os
import random
import logging
from twitchio.ext import commands

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PhraseBot(commands.Bot):
    def __init__(self):
        # Get environment variables
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        username = os.getenv('TWITCH_USERNAME')
        channel = os.getenv('TWITCH_CHANNEL')
        
        # Message counting config
        self.min_messages = int(os.getenv('MIN_MESSAGES', 5))
        self.max_messages = int(os.getenv('MAX_MESSAGES', 30))
        
        # Phrases to randomly append
        self.phrases = [
            "in bed",
            "<insewrt custom phrase here"
        ]
        
        # User-specific phrases (triggered when that user's message is selected)
        self.user_specific_phrases = {
            "someusername": "<insert custom phrase here>",
            "anotheruser": "<insert custom phrase here>",
            # Add more username: phrase pairs here
        }
        
        # Ignored usernames (bot won't count their messages or respond to them)
        self.ignored_users = {
            "nightbot",
            "streamelements", 
            "<insert custom phrase here>",
            # Add more usernames to ignore here (lowercase)
        }
        
        # Responses for Yes/No mentions
        self.yes_responses = [
            "<insert positive response>"
        ]
        
        self.no_responses = [
            "<insert negative response>"
        ]
        
        # Generic mention responses (when no yes/no detected)
        self.generic_mention_responses = [
            "Y<insert generic response>"
        ]
        
        # Message tracking
        self.message_count = 0
        self.next_trigger = random.randint(self.min_messages, self.max_messages)
        
        super().__init__(
            token=token,
            prefix='!',
            initial_channels=[channel]
        )
        
        logger.info(f"Bot initialized for channel: {channel}")
        logger.info(f"Will trigger after {self.next_trigger} messages.")
    
    async def event_ready(self):
        logger.info(f'Logged in as | {self.nick}')
        logger.info(f'User id is | {self.user_id}')
        logger.info(f'Monitoring channel: {self.connected_channels[0].name}')
        logger.info("Bot is ready and listening for messages!")
    
    async def event_message(self, message):
        # Ignore messages from the bot itself
        if message.echo:
            return
        
        # Ignore specific users
        username_lower = message.author.name.lower()
        if username_lower in self.ignored_users:
            logger.debug(f"Ignoring message from {message.author.name}")
            return
        
        logger.debug(f"Message received from {message.author.name}: {message.content}")
        
        # Check if bot is mentioned
        bot_mentioned = f"@{self.nick.lower()}" in message.content.lower()
        
        # Check if message is a reply to someone else (starts with @ but NOT the bot's name)
        message_starts_with_mention = message.content.strip().startswith('@')
        if message_starts_with_mention:
            # Extract the first mentioned username
            first_word = message.content.strip().split()[0]
            first_mention = first_word.lstrip('@').lower()
            # If it's mentioning someone other than the bot, it's a reply to that person
            if first_mention != self.nick.lower():
                logger.debug(f"Message is a reply to @{first_mention}, ignoring")
                # Don't return yet - we still want to count this message for the phrase trigger
                bot_mentioned = False
        
        if bot_mentioned:
            await self.handle_mention(message)
            return
        
        # Ignore commands
        if message.content.startswith('!'):
            await self.handle_commands(message)
            return
        
        # Increment message counter
        self.message_count += 1
        logger.info(f"Message count: {self.message_count}/{self.next_trigger}")
        
        # Check if we should trigger the phrase
        if self.message_count >= self.next_trigger:
            await self.send_phrase_message(message)
            
            # Reset counter and set new random trigger
            self.message_count = 0
            self.next_trigger = random.randint(self.min_messages, self.max_messages)
            logger.info(f"Phrase sent! Next trigger in {self.next_trigger} messages.")
    
    async def send_phrase_message(self, original_message):
        # Check if this user has a specific phrase
        username_lower = original_message.author.name.lower()
        if username_lower in self.user_specific_phrases:
            phrase = self.user_specific_phrases[username_lower]
            logger.info(f"Using user-specific phrase for {original_message.author.name}")
        else:
            # Pick a random phrase
            phrase = random.choice(self.phrases)
        
        # Get the original message content
        content = original_message.content.strip()
        
        # Remove trailing punctuation to add phrase before it
        punctuation = ''
        if content and content[-1] in '.!?':
            punctuation = content[-1]
            content = content[:-1]
        
        # Construct the new message
        new_message = f"{content} {phrase}{punctuation}"
        
        logger.info(f"Sending phrase message: {new_message}")
        
        # Send to chat
        channel = original_message.channel
        await channel.send(new_message)
    
    async def handle_mention(self, message):
        """Handle when the bot is mentioned with Yes/No"""
        content_lower = message.content.lower()
        
        # Check for "no" variations
        no_keywords = ['no', 'nope', 'nah', 'negative', 'disagree', 'wrong']
        if any(keyword in content_lower for keyword in no_keywords):
            response = random.choice(self.no_responses)
            logger.info(f"Bot mentioned with 'No' - responding: {response}")
            await message.channel.send(f"@{message.author.name} {response}")
            return
        
        # Check for "yes" variations
        yes_keywords = ['yes', 'yeah', 'yep', 'yup', 'agree', 'correct', 'right', 'true']
        if any(keyword in content_lower for keyword in yes_keywords):
            response = random.choice(self.yes_responses)
            logger.info(f"Bot mentioned with 'Yes' - responding: {response}")
            await message.channel.send(f"@{message.author.name} {response}")
            return
        
        # Generic mention without yes/no
        logger.info(f"Bot mentioned without yes/no: {message.content}")
        response = random.choice(self.generic_mention_responses)
        await message.channel.send(f"@{message.author.name} {response}")
    
    @commands.command(name='phrasestats')
    async def phrase_stats(self, ctx):
        """Shows stats about the phrase bot"""
        remaining = self.next_trigger - self.message_count
        await ctx.send(f"Messages until next phrase: {remaining} | Total phrases: {len(self.phrases)}")
    
    @commands.command(name='phrases')
    async def list_phrases(self, ctx):
        """Lists all possible phrases"""
        phrase_list = ', '.join(self.phrases)
        await ctx.send(f"Possible phrases: {phrase_list}")

if __name__ == "__main__":
    bot = PhraseBot()
    bot.run()
