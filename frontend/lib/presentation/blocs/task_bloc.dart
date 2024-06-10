import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/usecases/submit_answers.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
part 'task_event.dart';
part 'task_state.dart';

class TaskBloc extends Bloc<TaskEvent, TaskState> {
  final SubmitAnswers submitAnswers;
  final ChatBloc chatBloc;

  TaskBloc(this.submitAnswers, this.chatBloc) : super(TaskInitial()) {
    on<InitializeTasksEvent>(_onInitializeTasks);
    on<CompleteTaskEvent>(_onCompleteTask);
    on<SubmitTasksEvent>(_onSubmitTasks);
  }

  void _onInitializeTasks(InitializeTasksEvent event, Emitter<TaskState> emit) {
    emit(TaskInProgress(event.tasks, 0));
  }

  void _onCompleteTask(CompleteTaskEvent event, Emitter<TaskState> emit) {
    final currentState = state as TaskInProgress;
    final tasks = List<Task>.from(currentState.tasks);
    tasks[event.taskIndex].userAnswers = event.userAnswers;
    tasks[event.taskIndex].completed = true;
    emit(TaskInProgress(tasks, currentState.currentTaskIndex + 1));
  }

  void _onSubmitTasks(SubmitTasksEvent event, Emitter<TaskState> emit) async {
    emit(TaskSubmissionInProgress());
    try {
      await submitAnswers(event.tasks);
      emit(TaskSubmissionSuccess());
      chatBloc.add(ProposeLessonEvent(true, 'german')); // Dispatch the new event
    } catch (error) {
      emit(TaskSubmissionFailure(error.toString()));
    }
  }
}