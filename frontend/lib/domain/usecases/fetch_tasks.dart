import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/repositories/chat_repository.dart';

class FetchTasks {
  final ChatRepository repository;

  FetchTasks(this.repository);

  Future<List<Task>> call(String chatId) {
    return repository.fetchTasks(chatId);
  }
}