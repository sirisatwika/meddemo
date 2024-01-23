from flask import Flask, request, jsonify
from flasgger import Swagger
from azure.iot.device import IoTHubDeviceClient, Message
import json

app = Flask(__name__)
Swagger(app)

def iothub_client_init(connection_string):
    return IoTHubDeviceClient.create_from_connection_string(connection_string)

@app.route('/send_data', methods=['POST'])
def send_data():
    """
    Send Data to IoT Hub
    ---
    parameters:
      - name: connection_string
        in: query
        type: string
        required: true
        description: IoT Hub connection string
      - name: request_data
        in: body
        required: true
        schema:
          type: object
          properties:
            energy:
              type: string
            voltage:
              type: string
            power:
              type: string
            current:
              type: string
    responses:
      200:
        description: Data sent successfully
      400:
        description: Bad Request
    """
    try:
        connection_string = request.args.get('connection_string')
        if not connection_string:
            return jsonify({"status": "error", "message": "Connection string is missing"})
        
        client = iothub_client_init(connection_string)

        # Get data from the request body
        request_data = request.get_json()
        if not request_data:
            return jsonify({"status": "error", "message": "No data provided in the request body"})

        # Construct message
        message = Message(json.dumps(request_data))

        # Send message to IoT Hub
        client.send_message(message)

        return jsonify({"status": "success", "message": "Data sent successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    app.run(debug=True, port=3000)

