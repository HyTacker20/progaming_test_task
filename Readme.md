# Task Management System Documentation

## Table of Contents

- [Introduction](#Introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Install Dependencies](#install-dependencies)
    - [Set Up Environment Variables](#set-up-environment-variables)
- [Docker Setup](#docker-setup)
    - [Building Docker Images](#building-docker-images)
    - [Running Docker Containers](#running-docker-containers)
- [Database Setup](#database-setup)
    - [Running Migrations](#running-migrations)
    - [Creating a Superuser](#creating-a-superuser)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
    - [Endpoints](#endpoints)
    - [Examples](#examples)
- [WebSocket Communication](#websocket-communication)
- [Testing](#testing)

---  

## Introduction

This is a **Task Management System** built with Django and Django REST Framework. It allows users to create, update, and
manage tasks with various statuses and priorities. The application also utilizes WebSocket communication via Django
Channels for real-time updates on task status changes.
  
---  

## Features

- **Task Management**: Create, read, update, and delete tasks.
- **Filtering**: Filter tasks by status, priority, and creation date.
- **Caching**: Implement caching for API responses to improve performance.
- **WebSocket Notifications**: Real-time notifications when a task's status changes.
- **Testing**: Comprehensive unit tests for views and WebSocket consumers.
- **Dockerized Environment**: Easy setup and deployment using Docker and Docker Compose.
- **Dependency Management**: Managed via Poetry for consistent and reproducible builds.

---  

## Project Structure

```  
├── app/  
│   ├── task_management_system/  
│   │   ├── __init__.py  
│   │   ├── asgi.py  
│   │   ├── settings.py  
│   │   ├── urls.py  
│   │   ├── wsgi.py  
│   │   ├── models.py  
│   │   ├── views.py  
│   │   ├── serializers.py  
│   │   ├── consumers.py  
│   │   ├── routing.py  
│   │   ├── mixins.py  
│   │   └── tests/  
│   │       ├── __init__.py   
│   │       ├── test_api.py  
│   │       ├── test_consumers.py  
│   │       └── test_cache.py  
│   ├── manage.py  
├── docker-compose.yml  
├── Dockerfile  
├── entrypoint.sh  
├── wait-for-postgres.sh  
├── .env  
├── pyproject.toml  
└── README.md  
```  

  
---  

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Poetry** installed for dependency management.

---  

## Installation

### Clone the Repository

```bash  
git clone https://github.com/yourusername/task-management-system.gitcd task-management-system
```
### Install Dependencies  
  
I use **Poetry** for dependency management.  
  
1. **Install Poetry** (if not already installed):  
  
   ```bash  
    curl -sSL https://install.python-poetry.org | python3 -
   ```  
  Or follow the instructions from the [Poetry official website](https://python-poetry.org/docs/#installation).
2. **Install Dependencies**:  
  
   ```bash  
    poetry install 
   ```  
  This will create a virtual environment and install all the required packages. 
### Set Up Environment Variables  
  
Create a `.env` file in the project root directory:  
  
```env  
# .env  
  
# PostgreSQL settings  
POSTGRES_DB=your_db_name  
POSTGRES_USER=your_db_user  
POSTGRES_PASSWORD=your_db_password  
POSTGRES_HOST=db  
POSTGRES_PORT=5432  
  
# Redis settings  
REDIS_HOST=redis  
REDIS_PORT=6379  
  
# Django settings  
SECRET_KEY=your_secret_key  
DEBUG=True  
```  

**Note:** Replace `your_db_name`, `your_db_user`, `your_db_password`, and `your_secret_key` with your actual
credentials.
  
---  

## Docker Setup

### Building Docker Images

Build the Docker images using Docker Compose:

```bash  
docker-compose build
```  
  
### Running Docker Containers  
  
Start the containers:  
  
```bash  
docker-compose up
```
  
This command will:  
  
- Start the **PostgreSQL** container.  
- Start the **Redis** container.  
- Build and start the **web** container for the Django application.  
  
---  
  
## Database Setup  
  

  
### Creating a Superuser  
  
Create a superuser to access the Django admin interface:  
  
```bash  
docker-compose exec web python manage.py createsuperuser
```  
  
Follow the prompts to set up the superuser credentials.  
  
---  
  
## Running the Application  
  
With the Docker containers running, you can access the application at:  
  
```  
http://localhost:8000/
```  
  
To access the Django admin interface:  
  
```  
http://localhost:8000/admin/
```  
  
---  
  
## API Documentation  
  
### Endpoints  
  
- **List Tasks**: `GET /api/v1/tasks/`  
- **Retrieve Task**: `GET /api/v1/tasks/{id}/`  
- **Create Task**: `POST /api/v1/tasks/`  
- **Update Task**: `PUT /api/v1/tasks/{id}/`  
- **Partial Update Task**: `PATCH /api/v1/tasks/{id}/`  
- **Delete Task**: `DELETE /api/v1/tasks/{id}/`

### Filtering Tasks

The API supports filtering tasks based on the following fields:

- **Status**: Filter tasks by their status (`New`, `In progress`, `Completed`).
- **Priority**: Filter tasks by their priority (`Low`, `Medium`, `High`).
- **Created At**: Filter tasks by their creation date.

#### Filter Parameters

- `status`: Filter by task status.
- `priority`: Filter by task priority.
- `created_at`: Filter by creation date (supports date range filtering).

#### Examples

- **Filter by Status**:

  ```
  GET /api/v1/tasks/?status=New
  ```

- **Filter by Priority**:

  ```
  GET /api/v1/tasks/?priority=High
  ```

- **Filter by Status and Priority**:

  ```
  GET /api/v1/tasks/?status=In progress&priority=Medium
  ```

- **Filter by Creation Date Range**:

  ```
  GET /api/v1/tasks/?created_at__gte=2023-01-01&created_at__lte=2023-12-31
  ```

### Examples

#### Get Task List with Filters

```http
GET /api/v1/tasks/?status=New&priority=High
```
  
### Examples  
  
#### Get Task List  
  
```http  
GET /api/v1/tasks/  
```  

**Response:**

```json  
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Task One",
      "description": "First task description.",
      "status": "New",
      "priority": "High",
      "created_at": "2024-09-19T23:00:00Z",
      "updated_at": "2024-09-19T23:00:00Z"
    },
    {
      "id": 2,
      "title": "Task Two",
      "description": "Second task description.",
      "status": "In Progress",
      "priority": "Medium",
      "created_at": "2024-09-19T23:10:00Z",
      "updated_at": "2024-09-19T23:10:00Z"
    }
  ]
}  
```  

#### Create a New Task

```http  
POST /api/v1/tasks/  
Content-Type: application/json  
  
{  
 "title": "New Task", "description": "Description of the new task.", "status": "New", "priority": "Low"
 }  
```  

**Response:**

```json  
{
  "id": 3,
  "title": "New Task",
  "description": "Description of the new task.",
  "status": "New",
  "priority": "Low",
  "created_at": "2024-09-19T23:20:00Z",
  "updated_at": "2024-09-19T23:20:00Z"
}  
```  

#### Update a Task

```http  
PATCH /api/v1/tasks/3/  
Content-Type: application/json  
  
{  
 "status": "Completed"}  
```  

**Response:**

```json  
{
  "id": 3,
  "title": "New Task",
  "description": "Description of the new task.",
  "status": "Completed",
  "priority": "Low",
  "created_at": "2024-09-19T23:20:00Z",
  "updated_at": "2024-09-19T23:25:00Z"
}  
```  

  
---  

## WebSocket Communication

The application uses WebSocket to send real-time updates when a task's status changes.

- **WebSocket Endpoint**: `ws://localhost:8000/ws/tasks/status/`

### Example Usage

You can use a WebSocket client (like [WebSocket King](https://websocketking.com/)
or [websocat](https://github.com/vi/websocat)) or Postman to connect to the WebSocket endpoint.

When a task's status is updated, a message like the following will be sent:

```json  
{
  "message": "Task #3: status changed to Completed."
}  
```  

  
---  

## Testing

### Running Tests

To run the test suite, execute:

```bash  
docker-compose exec web python manage.py test
```  
  
This will run all unit tests for the application, including:  

- API tests  
- WebSocket consumer tests   
  
---  