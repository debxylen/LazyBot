# Lazy Bot 3.0

Lazy Bot is a multifunctional, fun, and interactive Discord bot designed to enhance user engagement within your server. Originally created in June 2020 by Conan for **Akashic Scans** (later renamed **Lazy Scans**), Lazy Bot quickly gained popularity for its variety of fun commands and useful moderation features. After a long hiatus, Lazy Bot was revamped in 2023 by Aadi into **Lazy Bot 2.0**, offering a more feature-rich and user-friendly experience.

The bot serves multiple purposes, from uplifting the mood of the community, tracking actions like hugs and respect, to providing mini-games such as Rock, Paper, Scissors. It also aids server management with birthday tracking, and even helps with decision-making using AI-powered responses.

---

### Features

#### Fun & Interaction Commands
- **F Help**: Displays an organized list of commands and their descriptions.
- **F/Yui F `<username>`**: Pays respect to a specific user by adding an "F" reaction. The bot sends a message displaying how many people have paid their respects.
- **F Action `<User>`**: Actions like **hug**, **pat**, **poke**, **punch**, **bite**, **bonk**, **cry**, **kick**, etc. The bot sends an animated gif based on the action and tracks it for leaderboard ranking.
- **F rps `<user>`**: Starts a Rock, Paper, Scissors (RPS) game where users can challenge each other (cannot challenge themselves).
- **F rps lb `<user>`**: Displays statistics on the Rock, Paper, Scissors games played between two users, showing wins, losses, and ties.
- **F Leaderboard**: Displays the leaderboard of various actions (e.g., hugs, kicks, RPS wins).
- **F Pop**: A game where users try to find the 💍 (ring).

#### AI and Fun Features
- **F yn `<Question>`**: Uses AI to randomly answer "Yes" or "No" to questions.

#### Moderation & Utility
- **Birthday Function**: Tracks birthdays and notifies the admin team when a birthday is coming up (in IST). Command: `F insert birthday`.
- **Role System (Alpha)**: Identifies and gives a role to active members, known as the **Alpha** role.

#### New Features and Enhancements
- **Leaderboard Customization**: More accessible leaderboard commands, e.g., **f lb hug**.
- **Challenge System**: Users can challenge others to games like RPS, with personalized prompts to encourage friendly competition.
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
4. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file to store your secrets:  
   ```
   TOKEN = DISCORD_BOT_TOKEN
   MONGO_URI = MONGODB_URL
   TENOR_KEY = TENOR_API_KEY
   TENOR_CLIENT = TENOR_CLIENT_ID
   ```
6. Run the bot:
   
   - Without a virtual environment:  
     ```bash
     python main.py
     ```
   - With a virtual environment (for Unix-based systems):  
     ```bash
     ./start.sh
     ```
   - With a virtual environment (Windows systems):  
     ```bash
     start.bat
     ```

---

### License

LazyBot 3.0 is licensed under the terms of the AGPL v3.0.  
Copyright (C) 2025 Universal Scans.  
For full licensing details, please refer to the [LICENSE](LICENSE) file.

---

**Lazy Bot 2.0** is designed to make your Discord server more interactive and enjoyable. From fun games to moderation tools, Lazy Bot brings a lot of useful features to enhance your community. Enjoy using the bot and have fun! 🎉
