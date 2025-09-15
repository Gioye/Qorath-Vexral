# Qorath Vexral
Qorath Vexral is a do-it-all open source discord bot (https://dsc.gg/qorath)
It might not be 100% open source, but atleast it mostly is.

## BDScript
This Is The Best Option For Qorath Vexral.
🧱 Prerequisites
- ✅ Downloading https://botdesignerdiscord.com/ (Required To Host The Bot!)
- ✅ A Discord account
- ✅ A Discord server where you have permission to add bots
- ✅ Your bot token (from the Discord Developer Portal)

You can also use the web app (https://app.botdesignerdiscord.com/), However you still need to download it to make the bot go online.

All you need to do is:
- Making a new BDScript 2 Bot
- Creating a new command
- Pasting the wanted code in that command
- Creating a command trigger
- Follow the instructions in the code's $c[] Code Block at the very top if there's one

  And you're done. now watch some ADs in the app to get your bot online.


## Python
Qorath Vexral No longer uses Python, but the Python code is still public.
🧱 Prerequisites
- ✅ Python 3.8 or newer installed
- ✅ A Discord account
- ✅ A Discord server where you have permission to add bots
- ✅ Your bot token (from the Discord Developer Portal)

🔹 1. Create your bot on Discord Developer Portal
Go to https://discord.com/developers/applications
Click "New Application"
Name your bot and click Create
On the left, click "Bot" → then click "Add Bot" → Confirm
Under TOKEN, click "Reset Token" (or Copy) to get your bot token.
Save this token somewhere secure. You’ll use it as an environment variable.

🔹 2. Invite the bot to your server
In the Developer Portal → Left menu → OAuth2 → URL Generator
Under OAuth2 scopes, check:
bot
Under OAuth2 > Bot Permissions, choose what you want the python code to do to your bot
Send Messages
Read Message History
Embed Links, etc.
Copy the generated link → paste it in your browser → invite the bot to your server.

🔹 3. Set up the Python environment
A. Install discord.py
In your terminal or command prompt:
`pip install -U discord.py`

🔹 4. Set Up "os.getenv("TOKEN")"
Install Python dotenv package:
`pip install python-dotenv`

Create a .env file in the same folder:
`TOKEN=your_bot_token_here`

Now, In The Python main.py Top (Everything before "os.getenv("TOKEN")") you must replace it with:
```python
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import time
import re

load_dotenv()
```

🔹 5. Bot Time
Run this command in the folder you downloaded main.py: `python bot.py`

Now you're done that's it. if there's an error, update the Token Env. Variable.
