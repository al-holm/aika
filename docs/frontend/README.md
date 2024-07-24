# Frontend Overview

This document provides an overview of the frontend part of the application built using Flutter.
To install, see: [Setup Instructions](setup.md).

## Project Structure

- **data/**: Contains models, repositories, and data providers.
- **domain/**: Contains entities, repositories, and use cases.
- **presentation/**: Contains blocs, screens, widgets, and routes.

## Main Entry Point

- **main.dart**: The entry point of the Flutter application.

## Components
We used **Clean Architecture** Pattern as a template.
![](res/component_diagram_frontend.png)

## State Management

This application uses the BLoC (Business Logic Component) pattern for state management. Each BLoC handles a specific part of the application's state and business logic.

### BLoC Overview

- **Authentification BLoC**: Manages user authentication state.
- **Chat BLoC**: Manages the state of chat interactions.
- **Task BLoC**: Manages language learning tasks screens within the German chat.
- **Language Management BLoC**: Manages switching between differen languages for the UI components.

#### Detailed BLoC Documentation
For detailed information on each BLoC, refer to the specific documentation files:

- [Authentification BLoC](state_management/auth_bloc.md)
- [Chat BLoC](state_management/chat_bloc.md)
- [Task BLoC](state_management/task_bloc.md)