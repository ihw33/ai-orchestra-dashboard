# Real-time AI Chat Bridge Documentation

## Overview
The AI Chat Bridge is a real-time communication system that enables multiple AI agents to collaborate through WebSocket connections. It provides both WebSocket and REST API interfaces for flexible integration.

## Architecture

### Core Components

1. **AIChatBridge** - Main service managing agent communication
2. **ChatBridgeWebSocketHandler** - WebSocket connection handler
3. **FastAPI Router** - REST API endpoints and WebSocket endpoint
4. **Message Queue** - Asynchronous message processing system

### Data Models

#### AIAgent
```python
{
    "agent_id": "uuid",
    "name": "Claude-PM",
    "role": "pm",  # pm, frontend, backend, architect, qa
    "status": "online",  # online, offline, error, blocked
    "last_seen": "2025-08-21T22:30:00",
    "current_task": "TASK-001"  # or null
}
```

#### ChatMessage
```python
{
    "message_id": "uuid",
    "sender_id": "uuid",
    "sender_name": "Claude-PM",
    "recipient_id": "uuid",  # null for broadcast
    "message_type": "chat",  # chat, command, status, task, response, error, heartbeat, broadcast
    "content": "Message content",
    "metadata": {},
    "timestamp": "2025-08-21T22:30:00"
}
```

## API Endpoints

### WebSocket Endpoint
- **URL**: `ws://localhost:8000/api/chat-bridge/ws`
- **Purpose**: Real-time bidirectional communication

### REST Endpoints

#### Agent Management
- `POST /api/chat-bridge/agents/register` - Register new agent
- `DELETE /api/chat-bridge/agents/{agent_id}` - Unregister agent
- `GET /api/chat-bridge/agents` - List all agents
- `GET /api/chat-bridge/agents/{agent_id}` - Get agent status

#### Messaging
- `POST /api/chat-bridge/messages/send` - Send message
- `POST /api/chat-bridge/messages/broadcast` - Broadcast to all
- `GET /api/chat-bridge/messages/history` - Get message history

#### Task Management
- `POST /api/chat-bridge/tasks/assign` - Assign task to agent
- `PUT /api/chat-bridge/tasks/{task_id}/status` - Update task status
- `GET /api/chat-bridge/tasks` - List all tasks

#### System
- `GET /api/chat-bridge/status` - Get system status
- `GET /api/chat-bridge/health` - Health check
- `GET /api/chat-bridge/ws/example` - WebSocket usage examples

## WebSocket Protocol

### Connection Flow

1. **Connect** to WebSocket endpoint
2. **Register** agent with name and role
3. **Receive** registration confirmation with agent_id
4. **Exchange** messages with other agents
5. **Send** periodic heartbeats (recommended every 30s)
6. **Disconnect** when done

### Message Types

#### Registration (Client → Server)
```json
{
    "type": "register",
    "name": "Gemini-Frontend",
    "role": "frontend"
}
```

#### Registration Response (Server → Client)
```json
{
    "type": "registered",
    "agent_id": "uuid-here",
    "team_status": { /* current team status */ }
}
```

#### Chat Message (Client → Server)
```json
{
    "type": "chat",
    "recipient_id": null,  // null for broadcast
    "content": "Hello team!",
    "metadata": {}
}
```

#### Task Update (Client → Server)
```json
{
    "type": "task_update",
    "task_id": "TASK-001",
    "status": "in_progress",
    "metadata": {
        "progress": 50,
        "notes": "Halfway complete"
    }
}
```

#### Heartbeat (Client → Server)
```json
{
    "type": "heartbeat"
}
```

#### Incoming Message (Server → Client)
```json
{
    "message_id": "uuid",
    "sender_id": "uuid",
    "sender_name": "Claude-PM",
    "recipient_id": null,
    "message_type": "chat",
    "content": "Team standup starting",
    "metadata": {},
    "timestamp": "2025-08-21T22:30:00"
}
```

## Usage Examples

### Python WebSocket Client
```python
import asyncio
import websockets
import json

async def ai_agent():
    uri = "ws://localhost:8000/api/chat-bridge/ws"
    async with websockets.connect(uri) as websocket:
        # Register
        await websocket.send(json.dumps({
            "type": "register",
            "name": "MyAI",
            "role": "backend"
        }))
        
        # Wait for registration
        response = await websocket.recv()
        data = json.loads(response)
        agent_id = data["agent_id"]
        
        # Send message
        await websocket.send(json.dumps({
            "type": "chat",
            "recipient_id": None,
            "content": "Hello team!",
            "metadata": {}
        }))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(ai_agent())
```

### JavaScript WebSocket Client
```javascript
const ws = new WebSocket('ws://localhost:8000/api/chat-bridge/ws');

ws.onopen = () => {
    // Register agent
    ws.send(JSON.stringify({
        type: 'register',
        name: 'WebUI',
        role: 'frontend'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'registered') {
        console.log('Registered with ID:', data.agent_id);
        
        // Send a message
        ws.send(JSON.stringify({
            type: 'chat',
            recipient_id: null,
            content: 'Frontend connected!',
            metadata: {}
        }));
    } else {
        console.log('Message:', data);
    }
};

// Send heartbeat every 30 seconds
setInterval(() => {
    ws.send(JSON.stringify({ type: 'heartbeat' }));
}, 30000);
```

### REST API Usage (curl)
```bash
# Register agent
curl -X POST "http://localhost:8000/api/chat-bridge/agents/register" \
     -H "Content-Type: application/json" \
     -d '{"name": "CLI-Agent", "role": "backend"}'

# Send message
curl -X POST "http://localhost:8000/api/chat-bridge/messages/send" \
     -H "Content-Type: application/json" \
     -d '{
       "sender_id": "agent-uuid",
       "content": "Task completed",
       "recipient_id": null,
       "message_type": "chat"
     }'

# Get team status
curl "http://localhost:8000/api/chat-bridge/status"

# Assign task
curl -X POST "http://localhost:8000/api/chat-bridge/tasks/assign" \
     -H "Content-Type: application/json" \
     -d '{
       "task_id": "TASK-002",
       "agent_id": "agent-uuid",
       "description": "Implement user authentication",
       "priority": "high"
     }'
```

## Testing

### Run Test Client
```bash
# Run demo scenario
python backend/test_chat_bridge.py

# Run interactive client
python backend/test_chat_bridge.py interactive "MyAgent" "backend"
```

### Load Testing
```bash
# Use websocket-bench or similar tools
websocket-bench -c 10 -r 100 ws://localhost:8000/api/chat-bridge/ws
```

## Integration with AI Orchestra Dashboard

### PM Control Integration
The Chat Bridge integrates with the PM Control system to:
1. Relay GitHub events to relevant AI agents
2. Coordinate task assignments from issues
3. Broadcast status updates during workflows
4. Facilitate real-time collaboration

### Frontend Integration
```typescript
// React hook for chat bridge
import { useWebSocket } from './hooks/useWebSocket';

function AITeamChat() {
    const { messages, sendMessage, agentStatus } = useWebSocket(
        'ws://localhost:8000/api/chat-bridge/ws',
        'Frontend-UI',
        'frontend'
    );
    
    return (
        <ChatInterface
            messages={messages}
            onSend={sendMessage}
            agents={agentStatus}
        />
    );
}
```

## Monitoring and Debugging

### Health Check
```bash
curl http://localhost:8000/api/chat-bridge/health
```

### View Logs
```bash
# Backend logs
tail -f backend/logs/chat_bridge.log

# WebSocket connections
netstat -an | grep 8000
```

### Debug Mode
Set environment variable for verbose logging:
```bash
export DEBUG=true
python backend/app/main.py
```

## Performance Considerations

1. **Message Queue**: Asynchronous processing prevents blocking
2. **Heartbeat**: 30-second intervals to detect disconnections
3. **Timeout**: 60-second timeout for inactive agents
4. **Message History**: Limited to recent 1000 messages in memory
5. **Connection Limit**: Default max 100 concurrent WebSocket connections

## Security

1. **Authentication**: Implement token-based auth for production
2. **Rate Limiting**: Add rate limits per agent
3. **Message Validation**: Validate all incoming messages
4. **CORS**: Configure appropriate CORS settings
5. **TLS**: Use wss:// in production

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if backend is running: `curl http://localhost:8000/health`
   - Verify port 8000 is not blocked

2. **Registration Failed**
   - Ensure role is valid: pm, frontend, backend, architect, qa
   - Check agent name is not empty

3. **Messages Not Received**
   - Verify WebSocket connection is active
   - Check recipient_id is correct or null for broadcast
   - Ensure agent is registered and online

4. **Task Updates Not Working**
   - Verify task_id exists
   - Check agent has permission to update task
   - Ensure metadata is valid JSON

## Future Enhancements

1. **Authentication & Authorization**
   - JWT token validation
   - Role-based permissions

2. **Persistence**
   - Store messages in database
   - Task history tracking
   - Agent activity logs

3. **Advanced Features**
   - Message encryption
   - File/code snippet sharing
   - Voice/video channels
   - Screen sharing for debugging

4. **Scaling**
   - Redis pub/sub for multi-instance
   - Load balancing WebSocket connections
   - Horizontal scaling support

## Contributing

To add new features or fix bugs:
1. Create feature branch
2. Update tests in `test_chat_bridge.py`
3. Update this documentation
4. Submit PR with description

## License

Part of AI Orchestra Dashboard project.