from flask import Flask, request, jsonify
from flask_cors import CORS
from fetchai.crypto import Identity
from fetchai import fetch
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
import os
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)

CORS(app)

client_identity = None # agent address and other details of the client
dashboard_response = None # final url for the dashboard


def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the client identity from environment variables
        client_identity = Identity.from_seed(os.getenv("CLIENT_KEY"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        # Define the client agent's metadata
        readme = """
        <description>Frontend client that interacts with dashboard analytics agents</description>
        <use_cases>
            <use_case>Send data paths to analytics agents and receive dashboard URLs</use_case>
        </use_cases>
        <payload_requirements>
            <description>Expects responses with dashboard URLs</description>
            <payload>
                <requirement>
                    <parameter>data_path</parameter>
                    <description>Path to the dataset for analysis</description>
                </requirement>
            </payload>
        </payload_requirements>
        """

        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5002/api/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Dashboard Analytics Frontend Client",
            readme=readme
        )

        logger.info("Client agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise

# searching the agents which can create dashboard on agentverse
@app.route('/api/search-agents', methods=['GET'])
def search_agents():
    """Search for available dashboard agents"""
    try:
        # Fetch available agents (assuming this returns a dictionary)
        available_ais = fetch.ai('This agent generates visualizations for datasets and provides a dashboard URL.')
        print(f'---------------------{available_ais}----------------------')

        # Directly access the 'ais' list within 'agents'
        agents = available_ais.get('ais', [])
        print(f'----------------------------------{agents}------------------------------------')

        extracted_data = []
        for agent in agents:
            name = agent.get('name')  # Extract agent name
            address = agent.get('address')

           
            # Append formatted data to extracted_data list
            extracted_data.append({
                'name': name,
                'address': address,
            })

        # Format the response with indentation for readability
        response = jsonify(extracted_data)
        response.headers.add('Content-Type', 'application/json; charset=utf-8')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200

    except Exception as e:
        logger.error(f"Error finding agents: {e}")
        return jsonify({"error": str(e)}), 500

# route to send the csv data to the selected agent
@app.route('/api/send-data', methods=['POST'])
def send_data():
    """Send data path to the selected dashboard agent"""
    global dashboard_response
    dashboard_response = None

    try:
        # Parse the request payload
        data = request.json
        data_path = data.get('dataPath')
        agent_address = data.get('agentAddress')

        # Validate the input data
        if not data_path or not agent_address:
            return jsonify({"error": "Missing data path or agent address"}), 400

        logger.info(f"Sending data path {data_path} to {agent_address}")

        # Prepare and send the payload to the agent
        payload = {"data_path": data_path} 
        send_message_to_agent(
            client_identity, # frontend client identity
            agent_address, # agent address where we have to send the address
            payload # payload which contains the data path
        )

        return jsonify({"status": "request_sent"})

    except Exception as e:
        logger.error(f"Error sending data path: {e}")
        return jsonify({"error": str(e)}), 500


# app route to get the generated dashboard's url 
@app.route('/api/get-dashboard-response', methods=['GET'])
def get_dashboard_response():
    """Get the most recent dashboard response."""
    global dashboard_response
    try:
        if dashboard_response:
            response = dashboard_response
            dashboard_response = None  # Clear the response after sending
            return jsonify(response)
    except Exception as e:
        logger.error(f"Error getting dashboard response: {e}")
        return jsonify({"error": str(e)}), 500

# app route to get recieve the messages on the agent
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages from the dashboard agent."""
    global dashboard_response
    try:
        # Parse the incoming webhook message
        data = request.get_data().decode("utf-8")
        logger.info("Received dashboard response")

        message = parse_message_from_agent(data)
        dashboard_response = message.payload

        logger.info(f"Processed dashboard response: {dashboard_response}")
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

# function to start the flask server
def start_server():
    """Start the Flask server."""
    try:
        # Load environment variables
        load_dotenv()
        init_client()
        app.run(host="0.0.0.0", port=5002)
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    start_server()
