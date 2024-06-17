import 'dart:convert';
import 'package:frontend/data/models/message_model.dart';
import 'package:frontend/data/models/task_model.dart';
import 'package:http/http.dart' as http;

class ChatDataProvider {
  final String baseUrl;

  ChatDataProvider(this.baseUrl);

  Future<MessageModel> sendMessage(
    String chatId, MessageModel userMessage) async {
    print('sending message..');
    final response = await http.post(
      Uri.parse('$baseUrl/chat/$chatId'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(userMessage.toJson()),
    );
    print(response.statusCode);
    if (response.statusCode == 201) {
      final dynamic data = json.decode(response.body)['message'];
      MessageModel model = MessageModel.fromJson(data);
      return model;
    } else {
      throw Exception('Failed to fetch a response');
    }
  }

  Future<void> sendImage(String chatId, String imagePath) async {
    final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/chats/$chatId/messages'));
    request.files.add(await http.MultipartFile.fromPath('image', imagePath));
    final response = await request.send();

    if (response.statusCode != 200) {
      throw Exception('Failed to send image');
    }
  }

  Future<MessageModel> fetchLesson(String chatId) async {
    print('fetching lesson');
    final response = await http.get(
      Uri.parse('$baseUrl/chat/lesson')
      );
     if (response.statusCode == 200) {
      final dynamic data = json.decode(response.body);
      final tasksJson = data['tasks'] as List<dynamic>;
      final tasks = tasksJson.map((taskJson) => TaskModel.fromJson(taskJson)).toList();
      return  MessageModel(
        text: data['text'], 
        userID:'lesson', 
        messageID: '', 
        role: 'bot', 
        timestamp: DateTime.now(),
        hasTasks: true,
        tasks: tasks,
      );
    } else {
      throw Exception('Failed to fetch a lesson');
    }
  }
}

// Thought - create for lessons antoher model (maybe inheritance from message model)