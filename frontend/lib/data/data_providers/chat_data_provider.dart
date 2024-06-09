import 'dart:convert';
import 'package:frontend/data/models/message_model.dart';
import 'package:http/http.dart' as http;

class ChatDataProvider {
  final String baseUrl;

  ChatDataProvider(this.baseUrl);

  Future<MessageModel> sendMessage(
    String chatId, MessageModel userMessage) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat/$chatId'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(userMessage.toJson()),
    );
    print(response.statusCode);
    if (response.statusCode == 201) {
      final dynamic data = json.decode(response.body)['message'];
      MessageModel model = MessageModel(
        text: data['text'], 
        userID:data['userId'], 
        messageID: data['messageId'], 
        role: data['role'], 
        timestamp: DateTime.parse(data['timestamp']),
        );
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
    final response = await http.get(
      Uri.parse('$baseUrl/chat/lesson')
      );
    print(response.statusCode);
    print(response.body);
     if (response.statusCode == 200) {
      return  MessageModel.lessonFromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to fetch a lesson');
    }
  }
}