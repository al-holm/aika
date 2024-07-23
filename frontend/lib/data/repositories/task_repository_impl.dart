import 'package:frontend/data/data_providers/task_data_provider.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/repositories/task_repository.dart';

class TaskRepositoryImpl implements TaskRepository {
  final TaskDataProvider dataProvider;

  TaskRepositoryImpl(this.dataProvider);

  @override
  Future<void> submitUserAnswers(List<Task> tasks, String accessToken) {
    return dataProvider.submitUserAnswers(tasks, accessToken);
  }
}