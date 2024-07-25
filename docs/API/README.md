# API Documentation

## Table of Contents
- [API Gateway](#api-gateway)
  - [Authentication Endpoints](#authentication-endpoints)
    - [`POST /auth`](#post-auth)
  - [Chat Endpoints](#chat-endpoints)
    - [`POST /chat/german`](#post-chatgerman)
    - [`POST /chat/law`](#post-chatlaw)
    - [`GET /chat/lesson`](#get-chatlesson)
    - [`GET /chat/tasks`](#get-chattasks)
    - [`POST /chat/submit_answers`](#post-chatsubmit_answers)
- [User Microservice](#user-microservice)
  - [Auth Endpoints](#auth-endpoints)
    - [`POST /auth/login`](#post-authlogin)
    - [`POST /auth/register`](#post-authregister)
- [Curriculum Microservice](#curriculum-microservice)
  - [Lesson Endpoints](#lesson-endpoints)
    - [`GET /lesson/next`](#get-lessonnext)
    - [`GET /lesson/tasks`](#get-lessontasks)
    - [`POST /lesson/process_answers`](#post-lessonprocess_answers)
- [Agent Microservice](#agent-microservice)
  - [Agent Endpoints](#agent-endpoints)
    - [`POST /get_answer_german`](#post-get_answer_german)
    - [`POST /get_answer_law`](#post-get_answer_law)
    - [`POST /get_lesson_text`](#post-get_lesson_text)
    - [`GET /get_lesson_exercises`](#get-get_lesson_exercises)
---

## API Gateway

### Authentication Endpoints

#### `POST /auth`

- **Description**: Authenticates a user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string",
    "isSignUp": "bool"
  }
  ```
- **Response**:
    ```json
    {
    "accessToken": "string"
    }
    ```
### Chat Endpoints
#### `POST /chat/german`
- **Description**: Processes a German chat message.
- **Request Body**:
  ```json
  {
    "userId": "string",
    "messageId": "string",
    "role": "user",
    "timestamp": "string",
    "text": "string"
  }
  ```
- **Response**:
    ```json
    {
    "message": "string"
    }
    ```
#### `POST /chat/law`
- **Description**: Processes a "Law & Politics" chat message.
- **Request Body**:
  ```json
  {
    "userId": "string",
    "messageId": "string",
    "role": "user",
    "timestamp": "string",
    "text": "string"
  }
  ```
- **Response**:
    ```json
    {
    "message": "string"
    }
    ```
#### `GET /chat/lesson`
- **Description**: Get next German lesson. 
- **Response**:
    ```json
    {
    "text": "string",
    "audio": "string",
    "video": "string",
    "type": "string"
    }
    ```
#### `GET /chat/tasks`
- **Description**: Get a list of tasks for a generated lesson.
- **Response**:
    ```json
    {
    "tasks": [
        {
        "type": "TaskType",
        "id": 1,
        "lessonType": "string",
        "question": "string",
        "userAnswers": [["string"]],
        "solutions": ["string"]
        },
    ],
    "type": "string",
    "id": "int"
    }
    ```
#### `POST /chat/submit_answers`
- **Description**: Submit user answers for the generated tasks.
- **Request Body**:
    ```json
    {
    "tasks": [
        {
        "type": "TaskType",
        "id": "int",
        "lessonType": "string",
        "question": "string",
        "userAnswers": [["string"]],
        "solutions": ["string"],
        "lessonType": "string",
        },
    ],
    }
    ```

## User Microservice
### Auth Endpoints
#### `POST /auth/login`

- **Description**: Authenticates a registered user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string",
  }
  ```
- **Response**:
    ```json
    {
    "accessToken": "string"
    }
    ```
#### `POST /auth/register`

- **Description**: Authenticates a new user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string",
  }
  ```
- **Response**:
    ```json
    {
    "accessToken": "string"
    }
    ```

## Curriculum Microservice
### Lesson Endpoints
#### `GET /lesson/next`
- **Description**: Get next German lesson. 
- **Response**:
    ```json
    {
    "text": "string",
    "audio": "string",
    "video": "string",
    "type": "string"
    }
    ```
#### `GET /lesson/tasks`
- **Description**: Get a list of tasks for a generated lesson.
- **Response**:
    ```json
    {
    "tasks": [
        {
        "type": "TaskType",
        "id": 1,
        "lessonType": "string",
        "question": "string",
        "userAnswers": [["string"]],
        "solutions": ["string"]
        },
    ],
    "type": "string",
    "id": "int"
    }
    ```
#### `POST /lesson/process_answers`
- **Description**: Submit user answers for the generated tasks.
- **Request Body**:
    ```json
    {
    "tasks": [
        {
        "type": "TaskType",
        "id": "int",
        "lessonType": "string",
        "question": "string",
        "userAnswers": [["string"]],
        "solutions": ["string"],
        "lessonType": "string",
        },
    ],
    }
    ```

## Agent Microservice
### Agent Endpoints
#### `POST /get_answer_german`
- **Description**: Processes a German chat message.
- **Request Body**:
  ```json
  {
    "question": "string"
  }
  ```
- **Response**:
    ```json
    {
    "answer": "string"
    }
    ```
#### `POST /get_answer_german`
- **Description**: Processes a "Law & Politics" chat message.
- **Request Body**:
  ```json
  {
    "question": "string"
  }
  ```
- **Response**:
    ```json
    {
    "answer": "string"
    }
    ```
#### `POST /get_lesson_text`
- **Description**: Get next German lesson.
- **Request Body**:
  ```json
  {
    "request": "string"
  }
  ``` 
- **Response**:
    ```json
    {
    "text": "string",
    "audio": "string",
    "video": "string",
    }
    ```
#### `GET /get_lesson_exercises`
- **Description**: Get a list of tasks for a generated lesson.
- **Response**:
    ```json
    {
    "tasks": [
        {
        "type": "string",
        "id": 1,
        "lessonType": "string",
        "question": "string",
        "userAnswers": [["string"]],
        "solutions": ["string"]
        },
    ],
    }
    ```
