part of 'task_bloc.dart';

abstract class TaskEvent extends Equatable {
  const TaskEvent();

  @override
  List<Object> get props => [];
}

class InitializeTasksEvent extends TaskEvent {
  final List<Task> tasks;

  InitializeTasksEvent(this.tasks);

  @override
  List<Object> get props => [tasks];
}

class CompleteTaskEvent extends TaskEvent {
  final int taskIndex;
  final List<String> userAnswers;
  final bool goForward;

  CompleteTaskEvent(this.taskIndex, this.userAnswers, this.goForward);

  @override
  List<Object> get props => [taskIndex, userAnswers, goForward];
}

class SubmitTasksEvent extends TaskEvent {
  final List<Task> tasks;

  SubmitTasksEvent(this.tasks);

  @override
  List<Object> get props => [tasks];
}

class UpdateTaskAnswerEvent extends TaskEvent {
  final List<String> userAnswers;

  UpdateTaskAnswerEvent(this.userAnswers);

  @override
  List<Object> get props => [userAnswers];
}