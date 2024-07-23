# User Microservice Overview

The User Microservice handles user-related operations and data. It provides endpoints for user registration, authentication.

## Responsibilities

- Managing user accounts and profiles.
- Handling user authentication and registration.

## Services Interacted With

- **API Gateway**: Routes requests from clients to the user microservice.

# User Microservice Architecture

The architecture of the User Microservice is illustrated in the following diagram:

![Architecture](../res/user-microservice.svg)

# User Microservice Setup

## Prerequisites

- Node.js
- NestJS CLI

## Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/a-kholmovaia/aika.git
    ```

2. Navigate to the user-microservice directory:
    ```sh
    cd backend/user-microservice
    ```

3. Install dependencies:
    ```sh
    npm install
    ```
4. Run the service:
    ```sh
    npm run start
    ```

5. Run tests:
    ```sh
    npm run test
    ```