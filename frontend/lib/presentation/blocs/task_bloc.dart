import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/repositories/task_repository.dart';
part 'task_event.dart';
part 'task_state.dart';

class TaskBloc extends Bloc<TaskEvent, TaskState> {
  final TaskRepository taskRepository;

  TaskBloc(this.taskRepository) : super(TaskInitial()) {
    on<InitializeTasksEvent>(_onInitializeTasks);
    on<CompleteTaskEvent>(_onCompleteTask);
  }

  void _onInitializeTasks(InitializeTasksEvent event, Emitter<TaskState> emit) {
    emit(TaskInProgress(event.tasks, 0));
  }

  void _onCompleteTask(CompleteTaskEvent event, Emitter<TaskState> emit) async {
    final currentState = state as TaskInProgress;
    final tasks = List<Task>.from(currentState.tasks);
    tasks[event.taskIndex].userAnswers = event.userAnswers;
    tasks[event.taskIndex].completed = true;

    final allTasksCompleted = tasks.every((task) => task.completed);

    if (allTasksCompleted) {
      emit(TaskSubmissionInProgress());
      try {
        await taskRepository.submitUserAnswers(tasks);
        emit(TaskSubmissionSuccess());
      } catch (error) {
        emit(TaskSubmissionFailure(error.toString()));
      }
    } else {
      emit(TaskInProgress(tasks, currentState.currentTaskIndex + 1));
    }
  }
}