import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/repositories/chat_repository.dart';

class SendMessage {
  final ChatRepository repository;

  SendMessage(this.repository);

  Future<Message> call(
    String chatId, Message message, String accessToken) {
    return repository.sendMessage(
      chatId, message, accessToken);
  }
}