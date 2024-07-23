import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/repositories/chat_repository.dart';

class FetchMessageHistory{
  final ChatRepository repository;

  FetchMessageHistory(this.repository);

  Future<List<Message>> call(String chatId, String accessToken) {
    return repository.fetchMessageHistory(chatId, accessToken);
  }
}