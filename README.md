# Peerless

Peerless is an advanced and highly customizable Discord bot designed to make the management of Roblox sports leagues effortless. From handling teams, coaches, seasons, transactions, and a lot more, Peerless makes running a league smoother than ever.

## Features

Peerless provides a wide array of customization options to ensure that it fits perfectly with your league's needs. It allows for full league management, including team operations, league operations, transactions, and more. Additionally, it offers extensive settings for suspensions, demands, pickups, and many other essential league functionalities.

## Requirements

To run Peerless, ensure you have the latest versions of the following dependencies:

- **Redis** (for caching and data management)
- **PostgreSQL** (for database management)
- **Python** (primary language)

## Installation & Setup

1. Install Redis and PostgreSQL.
2. Clone this repository:
   ```sh
   git clone https://github.com/vxWrath/Peerless.git
   ```
3. Navigate to the project directory.
4. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Configure the bot settings in the `.env` file (see `.env.example`).
7. Set up the PostgreSQL database:
   - Create a PostgreSQL database.
   - Run the following SQL schema to initialize tables:
     ```sql
     CREATE TABLE players (
         id BIGINT NOT NULL PRIMARY KEY,
         blacklisted BOOL DEFAULT FALSE
     );
     
     CREATE TABLE leagues (
         id BIGINT NOT NULL PRIMARY KEY,
         teams JSONB DEFAULT '{}'::JSONB
     );
     
     CREATE TABLE player_leagues (
         player_id BIGINT REFERENCES players(id) ON DELETE CASCADE,
         league_id BIGINT REFERENCES leagues(id) ON DELETE CASCADE,
         demands INTEGER,
         PRIMARY KEY (player_id, league_id)
     );
     ```
8. Run the bot:
   ```sh
   python main.py
   ```
   
## Contact

- For support, join our Discord server: [Support Server](https://discord.gg/FsNK9y7MPg)
- Invite Peerless to your server: [Invite Link](https://discord.com/application-directory/1105640024113954829)