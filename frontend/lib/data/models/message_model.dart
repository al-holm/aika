
import 'package:frontend/domain/entities/message.dart';

class MessageModel {
  final String text;
  final String role;
  final String chatID;
  final MessageType messageType;
  final String audio;
  final String video;

  MessageModel({required this.text, required this.role, required this.chatID,
        this.messageType=MessageType.message, 
        this.audio='', this.video=''});
  
   factory MessageModel.fromJson(Map<String, dynamic> json) {
    return MessageModel(
      text: json['text'],
      role: json['role'],
      chatID: json['chatID']
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'text': text,
      'role' : role,
      'chatID' : chatID
    };
  }
  // Getters
  String get getText => text;
  String get getRole => role;
}