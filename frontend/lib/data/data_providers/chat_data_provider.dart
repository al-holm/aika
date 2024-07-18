import 'dart:convert';
import 'package:frontend/data/models/message_model.dart';
import 'package:frontend/data/models/task_model.dart';
import 'package:frontend/domain/entities/message.dart';
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
      MessageType type = MessageTypeExtension.fromString(data['type']);
      print(type);
      MessageModel model = MessageModel(
        text: data['text'], 
        userID:'lesson', 
        messageID: '', 
        role: 'bot', 
        timestamp: DateTime.now(),
        messageType: type,
        audio: type == MessageType.listening ? data['audio'] : '',
        video: type == MessageType.listeningVideo ? data['video'] : ''
      );
      print(model.video.length);
      return  model;
    } else {
      throw Exception('Failed to fetch a lesson');
    }
  }

Future<List<TaskModel>> fetchTasks(String chatId) async {
    print('fetching tasks');
    final response = await http.get(
      Uri.parse('$baseUrl/chat/tasks')
      );
     if (response.statusCode == 200) {
      final dynamic data = json.decode(response.body);
      final tasksJson = data['tasks'] as List<dynamic>;
      final tasks = tasksJson.map((taskJson) => TaskModel.fromJson(taskJson, data['id'], data['lessonType'])).toList();
      return tasks;
    } else {
      throw Exception('Failed to fetch a lesson');
    }
  }

  Future<List<MessageModel>> fetchMessageHistory(String chatId) async {
    print('fetching messages');
    final response = await http.get(Uri.parse('$baseUrl/chat/history:$chatId'));
    return []; // uncomment the code below as soon as server logics is done
    if (response.statusCode == 200) {
      final dynamic data = json.decode(response.body);
      final messagesJson = data['messages'] as List<dynamic>;
      final messages = messagesJson.map((messageJson) => MessageModel.fromJson(messageJson)).toList();
      return messages;
    } else {
      //throw Exception('Failed to fetch a lesson');
      if (chatId == 'law') {
        return [MessageModel(text: 'Test Message History Law', userID: 'bot', messageID: 'ffe', role: 'bot', timestamp: DateTime.now())];
      } else {
        return [MessageModel(text: 'Test Message History German', userID: 'bot', messageID: 'ffe', role: 'bot', timestamp: DateTime.now())];
      }
    }
  }
}

