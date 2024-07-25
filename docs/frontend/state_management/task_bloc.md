# Task BLoC

## Overview
The Task BLoC manages the state of tasks within the chat, especially for the German chat.

## Sequence Diagram
![](../res/task-bloc-seq.png)

## Dependencies
- **SubmitAnswers**: Use case for submitting user answers.

## Events
### InitializeTasksEvent
- **Properties**: `tasks`
- **Description**: Triggered to initialize tasks.

### CompleteTaskEvent
- **Properties**: `taskIndex`, `userAnswers`, `goForward`
- **Description**: Triggered when a task is completed.

### SubmitTasksEvent
- **Properties**: `tasks`
- **Description**: Triggered to submit all tasks.

### UpdateTaskAnswerEvent
- **Properties**: `userAnswers`
- **Description**: Triggered to update answers for the current task.

## States
### TaskInitial
- **Description**: Initial state of the task BLoC.

### TaskInProgress
- **Properties**: `tasks`, `currentTaskIndex`
- **Description**: State when tasks are in progress.

### TaskSubmissionInProgress
- **Description**: State when task submission is in progress.

### TaskSubmissionSuccess
- **Description**: State when task submission is successful.

### TaskSubmissionFailure
- **Properties**: `errorMessage`
- **Description**: State when task submission fails.