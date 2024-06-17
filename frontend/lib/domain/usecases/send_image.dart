import 'package:frontend/domain/repositories/chat_repository.dart';

class SendImage {
  final ChatRepository repository;

  SendImage(this.repository);

  Future<void> call(String chatId, String imagePath) {
    return repository.sendImage(chatId, imagePath);
  }
}