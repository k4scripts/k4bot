# k4bot
The bot used for administration and moderation in K4scripts Discord

## TODO
- [ ] Make the 'db' persistent, bind volumes or use a database
- [ ] Add a logging system

## Technical Information
This bot is written in Python 3.11.0 and uses the [Pycord library](https://pycord.dev/).

### Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| TOKEN | The bot token used to authenticate with Discord | |
| VERIFY_ROLE_ID | The ID of the role that is given to verified users | |
| TIMEZONE | The timezone used for datetime conversions | Europe/Amsterdam |
| DEBUG_GUILD | The ID of the guild to use for debugging | |

## Running the bot
Set the environment variables in a `.env` file

### Locally
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

### Docker
1. Build the Docker image
```bash
docker build -t k4bot .
```

2. Run the Docker container
```bash
docker run --env-file .env k4bot
```