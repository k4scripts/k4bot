# k4bot
The bot used for administration and moderation in K4scripts Discord.

## 📋 TODO
- [x] Make the 'db' persistent, bind volumes ~~or use a database~~
- [x] Add a logging system

## ❓ Technical Information
This bot is written in Python 3.11.0 and uses the [Pycord library](https://pycord.dev/).

### 🍃 Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| TOKEN | The bot token used to authenticate with Discord | |
| VERIFY_ROLE_ID | The ID of the role that is given to verified users | |
| TIMEZONE | The timezone used for datetime conversions | Europe/Amsterdam |
| GUILD_ID | The ID of the guild to use (for debugging) | |
| LOGGING_LEVEL | The level of logging to use | 2 |

#### 🪵 Logging Levels

| Level | Description |
| --- | --- |
| 1 | DEBUG |
| 2 | INFO |
| 3 | WARNING |
| 4 | ERROR |
| 5 | CRITICAL |

## 🤖 Running the bot
Set the environment variables in a `.env` file in the root of the project.

### 🧰 Locally (for development)
1. Create a virtual environment
```bash
python3.11 -m venv .venv
```

2. Activate the virtual environment
```bash
source .venv/bin/activate
```

3. Install the required packages
```bash
pip install -r requirements.txt
```

4. Run the bot
```bash
python3.11 src/main.py
```

### 🐋 Docker
1. Build the Docker image
```bash
docker build -t k4bot .
```

2. Run the Docker container
```bash
docker run -d --env-file .env --name k4bot --mount type=bind,source="$(pwd)"/db.json,target=/app/db.json k4bot
```
We bind the `db.json` file to the container to make the database persistent.<br>Docs: [Docker - Use bind mounts](https://docs.docker.com/storage/bind-mounts/)