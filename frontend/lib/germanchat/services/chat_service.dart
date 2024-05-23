import 'package:frontend/germanchat/services/metadata_service.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/message.dart';

class ChatService {
  final String apiUrl;

  ChatService({required this.apiUrl});

  String generateMessageBody(Message message) {
    return jsonEncode(<String, dynamic>{
      'message_text': message.getText(),
      'user_id': message.getUserID(),
      'message_id': message.getMessageID(),
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

    if (response.statusCode == 201) {
      final responseData = jsonDecode(response.body)['message'];
      if (responseData.containsKey('message_text')) {
        return Message(
          text: responseData['message_text'],
          userID: responseData['user_id'],
          messageID: responseData['message_id'],
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
