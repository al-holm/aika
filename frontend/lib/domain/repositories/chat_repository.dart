import 'package:frontend/domain/entities/message.dart';

abstract class ChatRepository {
  Future<Message> sendMessage(String chatId, String content);
  Future<void> sendImage(String chatId, String imagePath);
  Future<Message> fetchLesson(String chatId);
}