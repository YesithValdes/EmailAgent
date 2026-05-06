# Gmail Integration Tools

Connect your email assistant to Gmail and Google Calendar APIs.

## Graph

The `src/gmail_agent/email_agent.py` graph is configured to use Gmail tools.
  
You simply need to run the setup below to obtain the credentials needed to run the graph with your own email.

## Setup Credentials

### 1. Set up Google Cloud Project and Enable Required APIs

#### Enable Gmail and Calendar APIs

1. Go to the [Google APIs Library and enable the Gmail API](https://developers.google.com/workspace/gmail/api/quickstart/python#enable_the_api)
2. Go to the [Google APIs Library and enable the Google Calendar API](https://developers.google.com/workspace/calendar/api/quickstart/python#enable_the_api)

#### Create OAuth Credentials

1. Authorize credentials for a desktop application [here](https://developers.google.com/workspace/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application)
2. Go to Credentials → Create Credentials → OAuth Client ID
3. Set Application Type to "Desktop app"
4. Click "Create"

> Note: If using a personal email (non-Google Workspace) select "External" under "Audience"

<img width="1496" alt="Screenshot 2025-04-26 at 7 43 57 AM" src="https://github.com/user-attachments/assets/718da39e-9b10-4a2a-905c-eda87c1c1126" />

> Then, add yourself as a test user
 
5. Save the downloaded JSON file (you'll need this in the next step)

### 2. Set Up Authentication Files

1. Move your downloaded client secret JSON file to the `.secrets` directory

```bash
# Create a secrets directory
mkdir -p src/gmail_agent/tools/gmail/.secrets

# Move your downloaded client secret to the secrets directory
mv /path/to/downloaded/client_secret.json src/gmail_agent/tools/gmail/.secrets/secrets.json
```

2. Run the Gmail setup script

```bash
# Run the Gmail setup script
python src/gmail_agent/tools/gmail/setup_gmail.py
```

-  This will open a browser window for you to authenticate with your Google account
-  This will create a `token.json` file in the `.secrets` directory
-  This token will be used for Gmail API access

## Use With A Local Deployment

### 1. Run the Gmail Ingestion Script with Locally Running LangGraph Server

1. Once you have authentication set up, run LangGraph server locally:

```bash
langgraph dev
```

2. Run the ingestion script in another terminal with desired parameters:

```bash
python src/gmail_agent/tools/gmail/run_ingest.py --email tu-correo@gmail.com --minutes-since 1000 --graph-name email_agent
```

- By default, this will use the local deployment URL (http://127.0.0.1:2024) and fetch emails from the past 1000 minutes.
- It will use the LangGraph SDK to pass each email to the locally running email assistant.
- It will use the `email_agent` graph, which is configured to use Gmail tools.

#### Parameters:

- `--graph-name`: Name of the LangGraph to use (default for this project: "email_agent")
- `--email`: The email address to fetch messages from
- `--minutes-since`: Only process emails that are newer than this many minutes (default: 120)
- `--url`: URL of the LangGraph deployment (default: http://127.0.0.1:2024)
- `--rerun`: Process emails that have already been processed (default: false)
- `--early`: Stop after processing one email (default: false)
- `--include-read`: Include emails that have already been read (by default only unread emails are processed)
- `--skip-filters`: Process all emails without filtering

#### Troubleshooting:

- **Missing emails?** The Gmail API applies filters to show only important/primary emails by default. You can:
  - Increase the `--minutes-since` parameter to a larger value (e.g., 1000)
  - Use the `--include-read` flag to process emails marked as "read"
  - Use the `--skip-filters` flag to include all messages
  - Try running with all options to process everything: `--include-read --skip-filters --minutes-since 1000`

### 2. Connect to Agent Inbox

After ingestion, you can access your interrupted threads in Agent Inbox (http://localhost:3000):
* Deployment URL: http://127.0.0.1:2024
* Assistant/Graph ID: `email_agent`
* Name: `Mi Asistente`

## How Gmail Ingestion Works

The Gmail ingestion process works in three main stages:

### 1. CLI Parameters → Gmail Search Query

CLI parameters are translated into a Gmail search query:
- `--minutes-since 1440` → `after:TIMESTAMP` (emails from the last 24 hours)
- `--email you@example.com` → `to:you@example.com OR from:you@example.com`
- `--include-read` → removes `is:unread` filter (includes read messages)

### 2. Search Results → Thread Processing

For each message returned by the search:
1. The script obtains the thread ID
2. Using this thread ID, it fetches the **complete thread** with all messages
3. Messages in the thread are sorted by date to identify the latest message
4. Ingests it to the LangGraph API to run the node workflow.
