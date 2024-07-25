# Authentification BLoC

## Overview
The Authentification BLoC manages the state for user authentication, including login and registration.

## Sequence Diagram
![](../res/auth_bloc_seq.png)

## Dependencies
- **SendCredentials**: Use case for submitting user credentials.

## Events
### SendCredentialsEvent
- **Properties**: `username`, `password`, `isSignUp`
- **Description**: Triggered when the user submits their credentials.

## States
### AuthentificationRequired
- **Description**: Initial state.

### AuthentificationPending
- **Description**: State when authentication is in progress.

### AuthentificationSucceed
- **Properties**: `sessionToken`
- **Description**: State when authentication is successful.

### AuthentificationFailed
- **Properties**: `errorMessage`
- **Description**: State when authentication fails.
