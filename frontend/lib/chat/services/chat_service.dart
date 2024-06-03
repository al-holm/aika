import 'package:frontend/chat/services/metadata_service.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/message.dart';

class ChatService {
  final String apiUrl;

  ChatService({required this.apiUrl});

  String generateMessageBody(Message message) {
    return jsonEncode(<String, dynamic>{
      'text': message.getText(),
      'userId': message.getUserID(),
      'messageId': message.getMessageID(),
      'role': message.getRole(),
      'timestamp': message.getTimestamp().toIso8601String(),
    });
  }

  Future<Message?> sendMessage(Message message) async {
    final messageBody = generateMessageBody(message);
    final url = Uri.parse(apiUrl);

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: messageBody,
    );

    print('\n\n\n\n\nAAAAA');
    print(response.statusCode);

    if (response.statusCode == 201) {
      final responseData = jsonDecode(response.body)['message'];
      print(DateTime.parse(responseData['timestamp']));
      if (responseData.containsKey('text')) {
        return Message(
          text: responseData['text'],
          userID: responseData['userId'],
          messageID: responseData['messageId'],
          role: responseData['role'],
          timestamp: DateTime.parse(responseData['timestamp']),
        );
      }
    } else {
      print(response.statusCode);
    }
    return null;
  }

  Message buildMessage(String text, String role, String userId, [String userID_ = '']) {
    DateTime timestamp = MetadataService.getCurrentTimestamp();
    String messageID = MetadataService.generateMessageID();
    String userID = userID_ == '' ? userId : userID_;
    return Message(
      text: text,
      userID: userID,
      messageID: messageID,
      role: role,
      timestamp: timestamp,
    );
  }
}
