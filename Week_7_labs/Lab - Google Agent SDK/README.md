# Agent2Agent Project

A multi-skill agent system that demonstrates agent-to-agent communication with keyword-based routing logic.

## Prerequisites

Before starting, ensure you have Python installed:

```bash
python --version  # Should be 3.8+
```

If you don't have `uv` installed, install it first:

```bash
pip install uv
```

Verify the installation:
```bash
uv --version
```

## Quick Start

### 1. Project Setup

Clone and navigate to the project directory:
```bash
cd Agent2Agent-Project
```

### 2. Environment Setup

Create and activate a virtual environment:
```bash
# Create virtual environment
uv venv venv

# Activate the environment
venv\Scripts\activate
```

### 3. Start the Server

Open your first terminal and run:
```bash
uv run .
```

Wait for the following output:
```
Starting Multi-Skill Agent with skills:
  - Greet (id: hello_world)
  - Get Quote (id: quote)
INFO:     Uvicorn running on http://0.0.0.0:9999
```

### 4. Test the Agent

Open a second terminal and run:
```bash
uv run --active test_client.py
```

## How to Use

### Interactive Testing

The test client provides a user-friendly menu:

```
🤖 MULTI-SKILL AGENT TESTER
Choose what to test:
1. 🖐️  Greeting (hello, hi, hey)
2. 💪 Quote/Motivation (quote, inspire, motivate)
3. 🎲 Custom message
4. 🚀 Run all tests
5. ❌ Exit
```

### Testing Options

1. **Greeting Test**: Try messages like "hello", "hi", "hey"
2. **Quote Test**: Try messages like "quote", "inspire", "motivate"
3. **Custom Message**: Enter any message to test routing behavior
4. **Run All Tests**: Automatically test all functionalities
5. **Exit**: Close the test client

## File Structure

```
Agent2Agent-Project/
├── __main__.py          # Main server - sets up A2A agent with 2 skills
├── agent_executor.py    # Multi-skill executor with keyword-based routing logic
├── test_client.py       # Interactive test client for user-friendly testing
└── README.md           # Project documentation and setup guide
```

### File Descriptions

- **`__main__.py`**: Entry point that initializes the server with multi-skill agent capabilities
- **`agent_executor.py`**: Core logic for routing messages between different agent skills based on keywords
- **`test_client.py`**: Interactive testing interface for validating agent responses and routing behavior
- **`README.md`**: This documentation file

## Expected Output Examples

### Server Startup
```
Starting Multi-Skill Agent with skills:
  - Greet (id: hello_world)
  - Get Quote (id: quote)
INFO:     Uvicorn running on http://0.0.0.0:9999
DEBUG: Received message: 'hello'
DEBUG: Routing to greeting agent
```

### Client Interaction
```
🤖 MULTI-SKILL AGENT TESTER
Choose what to test:
1. 🖐️  Greeting (hello, hi, hey)
2. 💪 Quote/Motivation (quote, inspire, motivate)
3. 🎲 Custom message
4. 🚀 Run all tests
5. ❌ Exit
```

## Features

- **Multi-skill agent system** with keyword-based routing
- **Interactive testing interface** for easy validation
- **Real-time debugging** with message routing logs
- **Extensible architecture** for adding new agent skills

## Troubleshooting

- Ensure the server is running before starting the test client
- Check that port 9999 is available on your system
- Verify that your virtual environment is activated before running commands
- Make sure all dependencies are installed

## Development

To extend the project with new skills:
1. Add new skill definitions in `__main__.py`
2. Update routing logic in `agent_executor.py`
3. Test new functionality using `test_client.py`