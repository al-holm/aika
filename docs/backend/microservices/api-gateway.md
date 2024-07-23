# API Gateway Overview

The API Gateway is the entry point for all client requests in the microservice architecture. It routes requests to the appropriate microservice.

## Responsibilities

- Routing client requests to the appropriate microservice.
- Performing request validation and response formatting.
- Aggregating responses from multiple services when necessary.

# API Gateway Architecture

The architecture of the API Gateway is illustrated in the following diagram:

![Architecture](../res/api_gateway.png)

## Services Interacted With

- **Curriculum Microservice**: Manages curriculum-related operations and data.
- **User Microservice**: Handles user-related operations & authentification and data.
- **Agent Microservice**: Performs specialized tasks such as LLM-driven question-answering, lesson & exercises creation.

# API Gateway Setup

## Prerequisites

- Node.js
- NestJS CLI

## Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepo.git
    ```

2. Navigate to the api-gateway directory:
    ```sh
    cd backend/api-gateway
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