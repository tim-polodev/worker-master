# Worker Master

Worker Master is a FastAPI-based worker tasks management service.

## Prerequisites

- Python 3.13+
- MongoDB instance
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tim-polodev/worker-master.git
   cd worker-master
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Configuration

Create a `.env` file in the root directory and configure the following environment variables:

```env
MONGO_DB_HOST=your_mongodb_host
MONGO_DB_PORT=27017
MONGO_DB_USER=your_username
MONGO_DB_PASSWORD=your_password
MONGO_DB_NAME=tasks
REQUEST_LIMITER=5/minute
```

## Running the Application

Start the FastAPI server using `uvicorn`:

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive documentation (Swagger UI) can be found at `http://localhost:8000/docs`.

## API Endpoints

### Tasks

#### Create a Task

- **URL**: `/api/v1/tasks`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "title": "Send Email",
    "command": "python send_email.py",
    "description": "Send weekly report",
    "recipient_emails": ["user@example.com"]
  }
  ```
- **Response**: `201 Created`

#### Get Task List

- **URL**: `/api/v1/tasks`
- **Method**: `GET`
- **Query Parameters**:
    - `limit` (int, default=10): Number of tasks per page.
    - `page` (int, default=1): Page number.
    - `sort_by` (string, default="created_at"): Field to sort by.
    - `sort_direction` (asc|desc, default="desc"): Sort direction.
- **Response**: `200 OK`

## Development

### Pre-commit Hooks

The project uses `pre-commit` to ensure code quality. To install the hooks:

```bash
uv run pre-commit install
```

### Running Tests

To run the tests:

```bash
uv run pytest
```

### TODOS

- [ ] Add authentication
    - [ ] Hard coded API key
    - [ ] With JWT
- [ ] Trigger scripts that run directly on local
- [ ] Trigger scripts that call remote APIs
- [ ] Trigger scripts that run on a remote AWS ECS Fargate cluster
- [ ] Add endpoint for updating tasks
- [ ] Allow scheduled tasks
