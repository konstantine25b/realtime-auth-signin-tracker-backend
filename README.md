# Backend of Full-Stack Web Application with Django, GraphQL, and ReactJS

## Overview

This project is a full-stack web application utilizing Django for the backend and ReactJS for the frontend. The application includes user authentication, registration, and sign-in counting functionality. It features real-time updates for both personal and global sign-in counts and notifies users when the global sign-in count reaches a specific threshold.

## Technologies Used

- **Django**: High-level Python web framework.
- **Django Channels**: Adds WebSocket support to Django.
- **Redis**: In-memory data structure store used as a message broker.
- **Graphene-Django**: Integrates GraphQL with Django.
- **GraphQL JWT**: Provides JSON Web Token (JWT) authentication for GraphQL.

## Features

- **GraphQL Server**: Implements queries, mutations, and subscriptions for interacting with data.
- **User Authentication**: Uses JWT tokens for secure login, logout, and registration.
- **SQLite Database**: Stores user information including credentials and personal sign-in counts.
- **Real-time Updates**: WebSockets with Django Channels and Redis enable live updates of personal and global sign-in counts.
- **Security**: Ensures personal sign-in counts are protected and accessible only to authenticated users.

## Setup

### Prerequisites

- Python 3.x
- Docker (for running Redis)

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/konstantine25b/realtime-auth-signin-tracker-backend
   cd realtime-auth-signin-tracker-backend
   
2. **Create a Virtual Environment and Activate It

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies

   ```sh
   pip install -r requirements.txt

4. Run Redis Server Using Docker
   
   Start a Redis container with the following command:
   ```sh
   docker run --rm -p 6379:6379 redis:7
   
5. **Apply Migrations
   ```sh
   python manage.py migrate

6. **Run the Development Server
   ```sh
   python manage.py runserver


##Contributing

###Contributions are welcome! Please open an issue or submit a pull request for any changes.

   
   


   
   

