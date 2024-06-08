import 'package:frontend/domain/repositories/chat_repository.dart';

class FetchLesson {
  final ChatRepository repository;

  FetchLesson(this.repository);

  Future<void> call(String chatId) {
    return repository.fetchLesson(chatId);
  }
}