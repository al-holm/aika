import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/entities/task.dart';

abstract class ChatRepository {
  Future<Message> sendMessage(
    String chatId, Message message);
  Future<void> sendImage(String chatId, String imagePath);
  Future<Message> fetchLesson(String chatId);
  Future<List<Task>> fetchTasks(String chatId);
}