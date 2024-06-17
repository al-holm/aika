import 'package:frontend/domain/entities/message.dart';

abstract class ChatRepository {
  Future<Message> sendMessage(
    String chatId, Message message);
  Future<void> sendImage(String chatId, String imagePath);
  Future<Message> fetchLesson(String chatId);
}