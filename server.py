from bottle import Bottle, request, response
import json

app = Bottle()
messages = []

@app.get('/messages')
def get_messages():
    response.content_type = 'application/json'
    return json.dumps(messages)

@app.post('/messages')
def post_message():
    data = request.json
    if not data or 'user' not in data or 'text' not in data:
        response.status = 400
        return json.dumps({'error': 'Invalid message format'})
    messages.append(data)
    return json.dumps({'status': 'Message received'})
