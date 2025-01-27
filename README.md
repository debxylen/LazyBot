# Lazy Bot 3.0
- **Respect Tracking**: Added tracking for "Respect count," showcasing who has received the most respect and when.

#### Commands

- **F Help**: Lists the available commands with their descriptions.
- **F/Yui F `<username>`**: Pays respect to the mentioned user.
- **F Action `<User>`**: Sends an anime-based gif for actions like hug, poke, kick, etc.
- **F Leaderboard**: Displays the leaderboard for various actions.
- **F rps**: Starts a game of Rock, Paper, Scissors.
- **F rps lb `<user>`**: Displays stats of a Rock, Paper, Scissors game between two users.
- **F Pop**: Fun pop game to find the 💍.
- **F insert birthday**: Allows users to add birthday information to the bot.

---

### Installation & Setup

To run **Lazy Bot 3.0** on your machine, follow these steps:

1. Clone the repository:  
   ```bash
   git clone https://github.com/UniversalScans/lazybot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd lazybot
   ```
   
3. As recommended, create a virtual environment: 
   ```bash
   python -m venv .
   "scripts/activate"
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file to store your secrets:
   ```
   TOKEN = DISCORD_BOT_TOKEN
   MONGO_URI = MONGODB_URL
   TENOR_KEY = TENOR_API_KEY
   TENOR_CLIENT = TENOR_CLIENT_ID
   ```

5. Run the bot
- Without a virtual environment:  
   ```bash
   python main.py
   ```
- With a virtual environment (for Unix-based systems):  
   ```bash
   ./start.sh
   ```
   *Windows users*:
   ```bash
   start.bat
   ```

### License
AGPL v3.0 License. See [LICENSE](LICENSE) for more details. 

---

**Lazy Bot 2.0** is designed to make your Discord server more interactive and enjoyable. From fun games to moderation tools, Lazy Bot brings a lot of useful features to enhance your community. Enjoy using the bot and have fun! 🎉
