import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/entities/task.dart';


abstract class ChatRepository {
  Future<Message> sendMessage(
    String chatId, Message message, String accessToken);
  Future<void> sendImage(String chatId, String imagePath);
  Future<Message> fetchLesson(String chatId, String accessToken);
  Future<List<Task>> fetchTasks(String chatId);
  Future<List<Message>> fetchMessageHistory(String chatId, String accessToken);
}