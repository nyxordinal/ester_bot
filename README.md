# Discord Bot Setup

Follow these steps to set up and run the Discord bot:

## Prerequisites

1. Obtain your Discord bot token.
2. Find your channel ID.

## Configuration

3. Duplicate the `.env.example` file and rename it to `.env`.

4. Open the `.env` file and set the following values:
   - `DISCORD_TOKEN` with your Discord bot token.
   - `CHANNEL_ID` with your channel ID.

## Installing Required Packages

5. Install the required Python packages listed in the `requirements.txt` file by running the following command in your terminal:  
   `pip install -r requirements.txt`

## Running the Bot

6. Run the bot using the following command:  
   `python main.py`

## Docker Support

7. For Docker support, follow these additional steps:
   - Build the Docker image:  
     `docker build -t nyxordinal/ester-bot --platform linux/amd64 .`
   - Run the Docker container in the background:
     ```bash
     docker run -d --name mybot \
       -e DISCORD_TOKEN=<your-bot-token> \
       -e CHANNEL_ID=<your-channel-id> \
       -e USER_ID=<your-user-id> \
       ester-bot:latest
     ```
