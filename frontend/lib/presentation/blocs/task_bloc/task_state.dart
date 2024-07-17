part of 'task_bloc.dart';

abstract class TaskState extends Equatable {
  const TaskState();

  @override
  List<Object> get props => [];
}

class TaskInitial extends TaskState {}

class TaskInProgress extends TaskState {
  final List<Task> tasks;
  final int currentTaskIndex;

  TaskInProgress(this.tasks, this.currentTaskIndex);

  @override
  List<Object> get props => [tasks, currentTaskIndex];
}

class TaskSubmissionInProgress extends TaskState {}

class TaskSubmissionSuccess extends TaskState {}

class TaskSubmissionFailure extends TaskState {
  final String error;

  TaskSubmissionFailure(this.error);

  @override
  List<Object> get props => [error];
}
