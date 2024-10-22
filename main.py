from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)

# Function to send message
def send_message(access_token, group_id, message):
    url = f'https://graph.facebook.com/v12.0/{group_id}/messages'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'message': {'text': message}}
    
    response = requests.post(url, headers=headers, json=data)
    
    return response.status_code == 200

@app.route('/send_messages', methods=['POST'])
def send_messages():
    data = request.json
    access_token = data.get('access_token')
    group_id = data.get('group_id')
    messages = data.get('messages')
    speed = data.get('speed', 1)

    if not all([access_token, group_id, messages]):
        return jsonify({"error": "Missing parameters"}), 400

    for message in messages:
        success = send_message(access_token, group_id, message)
        if not success:
            return jsonify({"error": "Failed to send message"}), 500
        time.sleep(speed)

    return jsonify({"status": "Messages sent successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
