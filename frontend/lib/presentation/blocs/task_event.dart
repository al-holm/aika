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

  CompleteTaskEvent(this.taskIndex, this.userAnswers);

  @override
  List<Object> get props => [taskIndex, userAnswers];
}

class SubmitTasksEvent extends TaskEvent {
  final List<Task> tasks;

  SubmitTasksEvent(this.tasks);

  @override
  List<Object> get props => [tasks];
}