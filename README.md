# Twitch Random Phrase Bot

A customizable Twitch chatbot that adds random phrases to chat messages after a random number of messages, inspired by the popular **InBedBot**.

## Features

- 🎲 **Random Phrase Injection**: Automatically appends random phrases to chat messages after a configurable number of messages
- 👤 **User-Specific Phrases**: Set custom phrases that trigger when specific users' messages are selected
- 🚫 **Ignore List**: Exclude certain users (like other bots) from triggering phrases
- 💬 **Interactive Mentions**: Responds when mentioned with "yes", "no", or generic greetings
- ⚙️ **Fully Configurable**: Customize phrase lists, trigger ranges, and responses
- 🐳 **Docker-Ready**: Easy deployment with Docker Compose

## How It Works

The bot monitors chat and counts non-command messages. After a random number of messages (between your configured min/max), it takes the next message and appends a random phrase to it, then sends it back to chat.

**Example:**
```
User: "I love pizza"
Bot: "I love pizza in bed"
```

After 15-25 more messages...
```
User: "That was awesome"
Bot: "That was awesome at Romans"
```

## Prerequisites

- Docker and Docker Compose installed
- A Twitch account for your bot
- OAuth token for the bot account

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/twitch-phrase-bot.git
cd twitch-phrase-bot
```

### 2. Get Your Twitch OAuth Token

1. Create a dedicated Twitch account for your bot (recommended) or use an existing account
2. Visit [Twitch Token Generator](https://twitchtokengenerator.com/)
3. Log in with your bot account
4. Generate a token with **chat:read** and **chat:write** scopes
5. Copy the OAuth token (starts with `oauth:`)

### 3. Configure the Bot

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your details:

```env
# Twitch Bot Configuration
TWITCH_USERNAME=your_bot_username
TWITCH_OAUTH_TOKEN=oauth:your_oauth_token_here
TWITCH_CHANNEL=channel_to_monitor

# Message trigger range (bot will randomly pick between these values)
MIN_MESSAGES=5
MAX_MESSAGES=30
```

### 4. Customize Phrases (Optional)

Edit `bot/bot.py` to customize the bot's behavior:

#### Random Phrases
```python
self.phrases = [
    "in bed",
    "<insert custom phrase here>",
    "<insert custom phrase here>",
]
```

#### User-Specific Phrases
```python
self.user_specific_phrases = {
    "username": "<insert custom phrase here>",
    "anotheruser": "<insert custom phrase here>",
}
```

#### Ignored Users
```python
self.ignored_users = {
    "nightbot",
    "streamelements",
    "<insert bot name to ignore>",
}
```

#### Yes/No/Generic Responses
```python
self.yes_responses = [
    "<insert positive response>",
]

self.no_responses = [
    "<insert negative response>",
]

self.generic_mention_responses = [
    "<insert generic response>",
]
```

### 5. Run the Bot

```bash
docker-compose up -d
```

### 6. Check Logs

```bash
docker-compose logs -f twitch-bot
```

You should see:
```
Logged in as | your_bot_username
User id is | 123456789
Monitoring channel: your_channel
Bot is ready and listening for messages!
```

## Commands

Users can interact with the bot using these commands:

- `!phrasestats` - Shows how many messages until the next phrase trigger
- `!phrases` - Lists all possible phrases the bot can use

## Configuration Details

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TWITCH_USERNAME` | Your bot's Twitch username | Required |
| `TWITCH_OAUTH_TOKEN` | OAuth token starting with `oauth:` | Required |
| `TWITCH_CHANNEL` | Channel to monitor (lowercase) | Required |
| `MIN_MESSAGES` | Minimum messages before trigger | 5 |
| `MAX_MESSAGES` | Maximum messages before trigger | 30 |

### Customization Options

#### 1. Random Phrases
Located in `bot/bot.py` under `self.phrases`. These phrases are randomly selected and appended to messages.

**Tips:**
- You can use Twitch emote names (e.g., `Kappa`, `LUL`, `PogChamp`)
- Keep phrases short for better readability
- Add as many or as few as you want

#### 2. User-Specific Phrases
Located in `bot/bot.py` under `self.user_specific_phrases`. When the trigger lands on a message from a specified user, their custom phrase is always used instead of a random one.

**Format:**
```python
"username": "custom phrase for this user"
```

**Note:** Use lowercase usernames.

#### 3. Ignored Users
Located in `bot/bot.py` under `self.ignored_users`. Messages from these users won't count toward the trigger and won't receive responses.

**Common bots to ignore:**
- `nightbot`
- `streamelements`
- `moobot`
- `streamlabs`

#### 4. Mention Responses
The bot responds differently based on what you say when mentioning it:

- **Yes replies**: Triggered by words like "yes", "yeah", "yep", "agree", "correct"
- **No replies**: Triggered by words like "no", "nope", "nah", "disagree", "wrong"
- **Generic replies**: When mentioned without yes/no keywords

### Docker Network

By default, the bot connects to an external network called `npm_npm`. If you want to use a different network or create a new one:

```yaml
networks:
  your_network_name:
    external: true  # For existing networks
    # OR
    driver: bridge  # To create a new network
```

## Project Structure

```
twitch-phrase-bot/
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Example environment variables
├── bot/
│   └── bot.py             # Main bot code
└── README.md              # This file
```

## Troubleshooting

### Bot Not Connecting

1. **Check OAuth token**: Ensure it starts with `oauth:` and is valid
2. **Verify username**: Must match the account that generated the token
3. **Check channel name**: Should be lowercase
4. **View logs**: `docker-compose logs -f` for error messages

### Bot Not Responding

1. **Check if bot is in chat**: Look for the bot in the viewer list
2. **Verify permissions**: Bot account needs chat access in the channel
3. **Test commands**: Try `!phrasestats` to see if the bot responds
4. **Check ignored users**: Make sure you're not in the ignored list

### Bot Responding to Wrong Messages

- **Replies to others**: The bot ignores messages that start with `@someoneelse`
- **Commands**: Messages starting with `!` are treated as commands
- **Bot messages**: The bot ignores its own messages

### Token Issues

If you see authentication errors:
1. Generate a new token at [Twitch Token Generator](https://twitchtokengenerator.com/)
2. Make sure you're logged in as the bot account when generating
3. Update the token in your `.env` file
4. Restart the bot: `docker-compose restart`

## Updating the Bot

1. Pull latest changes: `git pull`
2. Rebuild the container: `docker-compose up --build -d`
3. Check logs: `docker-compose logs -f`

## Stopping the Bot

```bash
docker-compose down
```

## Advanced Configuration

### Using a Different Network

Edit `docker-compose.yml`:

```yaml
networks:
  my_custom_network:
    driver: bridge
```

### Persistent Data

The bot includes a volume for persistent data storage:

```yaml
volumes:
  - bot-data:/app/data
```

Currently unused but available for future features like statistics or logging.

### Modifying Trigger Logic

You can adjust how the bot selects messages in `bot/bot.py`:

- Change `self.min_messages` and `self.max_messages` ranges
- Modify punctuation handling in `send_phrase_message()`
- Add custom logic in `event_message()`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Inspiration

This bot was inspired by **InBedBot**, a popular Twitch bot that appends "in bed" to random messages. This project expands on that concept with customizable phrases, user-specific triggers, and interactive responses.

## License

[MIT License](LICENSE)

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs: `docker-compose logs -f`
3. Open an issue on GitHub with your logs and configuration (remove sensitive data!)

## Acknowledgments

- Inspired by [InBedBot](https://www.twitch.tv/inbedbot)
- Built with [TwitchIO](https://github.com/TwitchIO/TwitchIO)
- Powered by Docker

---

**Made by TheRMan with the help of ClaudeAI**
