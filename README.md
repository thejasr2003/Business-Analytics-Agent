# Data Visualization Dashboard Agent

An AI-powered system that automatically creates beautiful interactive dashboards from your data using AI and Python.

## What This Project Does

This project has two main parts:

1. **Dashboard Analytics Agent** - Receives your data and creates smart visualizations using AI (GPT)
2. **User Client** - Lets you send data and get back a link to your dashboard

The system automatically creates charts like pie charts, line graphs, and scatter plots from your data!

## What You Need Before Starting

- **Python 3.11 or newer** - Programming language
- **Virtual Environment** - A safe space for your project dependencies
- **Three API Keys** (you'll get these for free):
  - [OpenAI API Key](https://platform.openai.com/settings/profile/api-keys) - For AI/GPT features
  - [Fetch.ai API Key](https://agentverse.ai/profile/api-keys) - For agent communication
  - **Two random phrases** - One for the dashboard agent, one for the user client (any random text works)

## Installation

### Step 1: Copy the Project

```
git clone https://github.com/abhifetch/dashboard-agents.git
cd dashboard_agents
```

### Step 2: Create a Virtual Environment

Use these commands based on your computer type:

**For Windows:**

```
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**

```
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages

```
pip install -r requirements.txt
```

## Set Up Your API Keys

Create a file named `.env` in the main project folder. Add these lines with your actual API keys:

```
OPENAI_API_KEY="paste-your-openai-key-here"
AGENTVERSE_API_KEY="paste-your-fetch-api-key-here"
DASHBOARD_AGENT_KEY="any-random-text-here"
CLIENT_KEY="any-random-text-here"
```

**Where to find these:**

- OpenAI key: [Get it here](https://platform.openai.com/settings/profile/api-keys)
- Fetch.ai key: [Get it here](https://agentverse.ai/profile/api-keys)
- Random phrases: Just type anything (they help keep your agents consistent)

## Running the Project

### Step 1: Start the Dashboard Agent

Run this command in your terminal:

```
python data_analytics_client.py
```

This starts the AI agent that will process your data and create visualizations.

### Step 2: Start the User Client

In a new terminal, run:

```
python data_analytics_user.py
```

This starts the client where you can send your data. Both programs should run at the same time.

## How to Use

### Step 1: Find the Agent

Run this to see available agents:

```
curl -X GET http://localhost:5002/api/search-agents
```

You'll get back an agent address - copy it.

### Step 2: Send Your Data

Put your data file (like `data.csv`) in the same folder as the scripts, then run:

```
curl -X POST http://localhost:5002/api/send-data \
-H "Content-Type: application/json" \
-d '{
  "dataPath": "data.csv",
  "agentAddress": "paste-the-agent-address-here"
}'
```

### Step 3: Get Your Dashboard

Check for your dashboard link by running:

```
curl -X GET http://localhost:5002/api/get-dashboard-response
```

Success! You'll get a URL to view your interactive dashboard.

## See It In Action

Check out this [video demo](https://youtu.be/0tDdsuaSGu4) to see the dashboard in action!

## Need Help?

For more details about Fetch.ai, visit their [official GitHub](https://github.com/fetchai/fetchai)

---

**Happy Visualizing!** 📊
