
import 'package:frontend/domain/entities/message.dart';

class MessageModel {
  final String text;
  final String userID;
  final String messageID;
  final String role;
  final DateTime timestamp;
  final bool hasTasks;
  final MessageType type;

  MessageModel({required this.text, 
        required this.userID,
        required this.messageID, required this.role,
        required this.timestamp, this.hasTasks=false, this.type=MessageType.message});
  
   factory MessageModel.fromJson(Map<String, dynamic> json) {
    return MessageModel(
      text: json['text'],
      userID: json['userId'],
      messageID: json['messageId'],
      role: json['role'],
      timestamp: DateTime.parse(json['timestamp']),
      hasTasks: json['hasTasks'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'text': text,
      'userId': userID,
      'messageId': messageID,
      'timestamp': timestamp.toIso8601String(),
      'role' : role,
      'hasTasks' : hasTasks,
    };
  }
  // Getters
  String get getText => text;
  String get getUserID => userID;
  String get getMessageID => messageID;
  String get getRole => role;
  DateTime get getTimestamp => timestamp;
  bool get getGotTasks => hasTasks;
}