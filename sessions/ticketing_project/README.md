# Ticketing System

This is a **Django-based Ticketing System** designed to manage support tickets with role-based access control. The system allows **Admins**, **Agents**, and **Customers** to interact with tickets based on their roles. It includes features such as ticket creation, assignment, status updates, and commenting.

---

## Features

### Role-Based Access Control
- **Admin**:
  - Access the admin dashboard to view all tickets.
  - Assign tickets to agents.
  - Create agent accounts.
- **Agent**:
  - Access the agent dashboard to view tickets assigned to them.
  - Update ticket statuses.
  - Add comments to tickets (including internal notes visible only to agents/admins).
- **Customer**:
  - Create tickets and view their own tickets in the customer dashboard.

### Core Functionalities
- **Ticket Management**:
  - Customers can create tickets with a subject, description, and priority.
  - Admins can assign tickets to agents.
  - Agents can update ticket statuses and leave comments.
- **Comments**:
  - Agents can leave comments on tickets, with an option for internal notes visible only to agents/admins.
- **Dashboards**:
  - Admin Dashboard: View and manage all tickets.
  - Agent Dashboard: View and manage tickets assigned to the agent.
  - Customer Dashboard: View tickets created by the customer.

---

## Permission Checks

The system enforces strict role-based permissions:
- **Admin Dashboard**: Only accessible by superusers. Other users are redirected to their respective dashboards.
- **Agent Dashboard**: Only accessible by agents. Other users are redirected to their respective dashboards.
- **Customer Dashboard**: Only accessible by customers. Other users are redirected to their respective dashboards.
- **Ticket Creation**: Only customers can create tickets.
- **Ticket Assignment**: Only admins can assign tickets to agents.
- **Ticket Updates**: Only agents can update ticket statuses.
- **Comments**: Only agents can comment on tickets.

---

## Makefile Commands

The `Makefile` includes several useful commands for managing the project:

| Command                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `make compose.start`   | Build and start the application using Docker Compose.                      |
| `make compose.migrate` | Run database migrations.                                                   |
| `make compose.migrations` | Create new database migrations.                                         |
| `make createadmin`     | Create a superuser for the application.                                    |
| `make createusers`     | Automatically create one admin, one customer, and one agent with roles.    |
| `make logs-web`        | View logs for the web service.                                             |
| `make compose.collectstatic` | Collect static files for deployment.                                 |
| `make test`            | Run the test suite using `pytest`.                                         |

---

## Environment Variables

The `.env` file is used to configure the database connection. Below are the variables and their purposes:

| Variable            | Description                          |
|---------------------|--------------------------------------|
| `POSTGRES_HOST`     | Hostname of the PostgreSQL database. |
| `POSTGRES_USERNAME` | Username for the database.           |
| `POSTGRES_PASSWORD` | Password for the database.           |
| `POSTGRES_PORT`     | Port number for the database.        |
| `POSTGRES_DATABASE` | Name of the database.                |


# Dependencies

The project uses the following dependencies:

- **Django**: Web framework for building the application.
- **FastAPI**: Included for potential API extensions.
- **PostgreSQL**: Database backend.
- **Poetry**: Dependency management.
- **Uvicorn**: ASGI server for running the application.
- **WhiteNoise**: Static file serving in production.

### Development dependencies:
- **pytest**: For running tests.
- **pytest-django**: Django integration for pytest.
- **httpx**: For making HTTP requests in tests.
- **requests**: For additional HTTP request handling.

# How to Run the Project

### Clone the Repository:
```bash
    git clone <repository-url>
    cd ticketing_project
```


### Set Up the Environment:

Create a `.env` file in the project root and configure it as shown above.

Example `.env` file:
```env
POSTGRES_HOST=db
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=qwerty
POSTGRES_PORT=5432
POSTGRES_DATABASE=db
```

### Start the Application: 
Use the following command to build and start the application:
```bash
make compose.start
```

### Run Database Migrations: 
Apply the database migrations:
```bash
make compose.migrate
```

### Create Users: 
Automatically create one admin, one customer, and one agent:
```bash
make createusers
```

### Access the Application:

Open your browser and navigate to [http://localhost:8000/login/](http://localhost:8000/login/) to log in.

# Running Tests

To run the test suite, use the following command:
```bash
make test
```

This will execute all tests and ensure the application is functioning as expected.

# Project Structure

- **tickets/**: Contains the core application logic, including models, views, templates, and forms.
- **ticketing_system/**: Contains project-level settings and configurations.
- **Dockerfile**: Defines the Docker image for the application.
- **docker-compose.yaml**: Configures the services (web and database) for the application.
- **Makefile**: Provides commands for managing the project.

# Default Users

The `make createusers` command creates the following users:

| Role    | Username | Password  | Notes                                        |
|---------|----------|-----------|----------------------------------------------|
| Admin   | admin    | admin123  | Superuser with full access.                 |
| Customer| customer | customer123 | Can create and view their own tickets.      |
| Agent   | agent    | agent123  | Can manage assigned tickets.                |

# License

This project is licensed under the MIT License.
