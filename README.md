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

1. Clone the Repository**

   ```sh
   git clone https://github.com/konstantine25b/realtime-auth-signin-tracker-backend
   cd realtime-auth-signin-tracker-backend
   
2. Create a Virtual Environment and Activate It

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies

   ```sh
   pip install -r requirements.txt

4. Run Redis Server Using Docker 
   
   Open Docker Desktop and then start a Redis container with the following command in different (separate) terminal:
   ```sh
   docker run --rm -p 6379:6379 redis:7
   
5. Apply Migrations
   ```sh
   python manage.py migrate

6. Run the Development Server
   ```sh
   python manage.py runserver

## Managing Superuser Access

### Create Superuser

  1. To create a superuser for administrative tasks:
     
     ```sh
     python manage.py createsuperuser

Follow the prompts to set a username, email (optional), and password for the superuser.

## Access Django Admin

** Navigate to the Django admin interface in your web browser:

   http://127.0.0.1:8000/admin/
   
** Log in using the superuser credentials created earlier.

# Testing GraphQL Endpoints

To test the GraphQL endpoints defined in your schema, you can use various methods to interact with your GraphQL API.

## Using GraphQL Playground or GraphiQL

1. **Accessing GraphQL Playground/GraphiQL**

   - Start your Django development server:
     ```bash
     python manage.py runserver
     ```
   - Navigate to `http://localhost:8000/graphql` in your web browser to open GraphQL Playground or GraphiQL.
     
2. **Testing Some of the Queries and Mutations**

   - **Register Mutation:**
     ```graphql
     mutation {
       register(username: "your_username", password: "your_password") {
         user {
           id
           username
         }
         token
         refreshToken
       }
     }
     ```

   - **Login Mutation:**
     ```graphql
     mutation {
       login(username: "your_username", password: "your_password") {
         user {
           id
           username
           signInCount
         }
         token
         refreshToken
       }
     }
     ```

   - **Change Password Mutation:**
     ```graphql
     mutation {
       changePassword(username: "your_username", password: "your_password", newPassword: "new_password") {
         user {
           id
           username
         }
         success
         token
         refresh_token
       }
     }
     ```

   - **Querying Global Sign-in Count:**
     ```graphql
     query {
       globalSignInCount
     }
     ```

