import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/repositories/task_repository.dart';

class SubmitAnswers {
  final TaskRepository repository;

  SubmitAnswers(this.repository);

  Future<void> call(List<Task> tasks, String accessToken) {
    return repository.submitUserAnswers(tasks, accessToken);
  }
}