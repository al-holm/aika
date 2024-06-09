import 'package:frontend/domain/entities/task.dart';

abstract class TaskRepository {
  Future<void> submitUserAnswers(List<Task> tasks);
}