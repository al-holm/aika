# Backend Overview
For the server part we chose a microservice architecture consisting of four services:

- **API Gateway**: Entry point for all client requests.
- **Curriculum Microservice**: Manages curriculum-related operations and data for fetching lesson topics & updating progress.
- **User Microservice**: Handles user-related operations and data.
- **Agent Microservice**: Python-based microservice for specialized tasks such as LLM-driven question-answering, lesson & exercises creation.

## Architecture

Each microservice is designed to be independent and scalable, with its own database or/and dependencies.

![](res/backend.svg)

## Communication

- **API Gateway**: Uses HTTP/REST for communication with other services.
- **Inter-Service Communication**: Handled via HTTP/REST.

## Technologies

- **NestJS**: Used for API Gateway, Curriculum Microservice, and User Microservice.
- **Python (Flask)**: Used for the Agent Microservice.

## Documentation
- [API Gateway Documentation](microservices/api-gateway.md)
- [Curriculum Microservice Documentation](microservices/curriculum-microservice.md)
- [User Microservice Documentation](microservices/user-microservice.md)
- [Agent Microservice Documentation](microservices/agent-microservice.md)

## Getting Started

To get started, refer to the setup instructions in each microservice's documentation.