# Curriculum Microservice Overview

The Curriculum Microservice manages curriculum-related operations and data. It provides endpoints for creating lessons and tasks & updating user progress.

## Responsibilities

- Retrieving next uncompleted topic.
- Providing endpoints for curriculum operations.
- Processing user answers & updating user progress.

## Services Interacted With

- **API Gateway**: Routes requests from clients to the curriculum microservice.
- **Agent Microservice**: Provides AI/ML operations for advanced processing.

# Curriculum Microservice Architecture

The architecture of the Curriculum Microservice is illustrated in the following diagram:

![Architecture](../res/curriculum.png)

# Curriculum Microservice Setup

## Prerequisites

- Node.js
- NestJS CLI

## Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepo.git
    ```

2. Navigate to the curriculum-microservice directory:
    ```sh
    cd backend/curriculum-microservice
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