# ClickHouse MCP SSE Server

A FastAPI-based server that provides Server-Sent Events (SSE) interface for ClickHouse database operations using MCP (Model Control Protocol).

## Features

- FastAPI-based REST API
- Server-Sent Events (SSE) support
- ClickHouse database integration
- Docker deployment support

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Access to a ClickHouse server

## Environment Setup

Create a `.env` file in the project root with the following variables:

```env
CLICKHOUSE_HOST=your_clickhouse_host
CLICKHOUSE_PORT=your_clickhouse_port
CLICKHOUSE_USER=your_clickhouse_user
CLICKHOUSE_PASSWORD=your_clickhouse_password
CLICKHOUSE_DATABASE=your_clickhouse_database
```

## Local Development

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
python mcp_server.py
```

The server will be available at `http://localhost:8000`

## Docker Deployment

1. Build and run the container:

```bash
docker-compose up -d --build
```

2. Check container status:

```bash
docker-compose ps
```

3. View logs:

```bash
docker-compose logs -f
```

4. Stop the container:

```bash
docker-compose down
```

The server will be available at `http://localhost:8083`

## API Endpoints

- `/sse`: SSE endpoint for real-time communication
- `/messages`: Endpoint for message handling

## Project Structure

```
.
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── mcp_server.py          # Main application file
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not in version control)
```

## License

[Add your license information here]
