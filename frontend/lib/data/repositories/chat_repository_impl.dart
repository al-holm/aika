import 'package:frontend/data/data_providers/chat_data_provider.dart';
import 'package:frontend/data/models/message_model.dart';
import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/repositories/chat_repository.dart';

class ChatRepositoryImpl implements ChatRepository {
  final ChatDataProvider chatDataProvider;

  ChatRepositoryImpl(this.chatDataProvider);

  @override
  Future<Message> sendMessage(
    String chatId, Message message) async {
    MessageModel userMessage = MessageModel(
      text: message.text, userID: message.userID, 
      messageID: message.messageID, role: message.role, 
      timestamp: message.timestamp);
    final MessageModel messageModel = await chatDataProvider.sendMessage(
      chatId, userMessage);
    return Message(
      text: messageModel.text, userID: messageModel.userID, 
      messageID: messageModel.messageID, role: messageModel.role, 
      timestamp:messageModel.timestamp, hasTasks: messageModel.hasTasks);
  }

  @override
  Future<void> sendImage(String chatId, String imagePath) {
    return chatDataProvider.sendImage(chatId, imagePath);
  }

  @override
  Future<Message> fetchLesson(String chatId) async {
     final MessageModel messageModel = await chatDataProvider.fetchLesson(chatId);
     return Message(
      text: messageModel.text, userID: messageModel.userID, 
      messageID: messageModel.messageID, role: messageModel.role, 
      timestamp:messageModel.timestamp, hasTasks: messageModel.hasTasks,
      tasks: messageModel.tasks?.map(
        (taskModel) => Task(
          type: taskModel.type, 
          question: taskModel.question, 
          answerOptions: taskModel.answerOptions, 
          solutions: taskModel.solutions,
          id: taskModel.id,
          lessonType: taskModel.lessonType,
          )
        ).toList(),
      );
  }

}