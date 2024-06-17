import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/repositories/chat_repository.dart';

class FetchLesson {
  final ChatRepository repository;

  FetchLesson(this.repository);

  Future<Message> call(String chatId) {
    return repository.fetchLesson(chatId);
  }
}