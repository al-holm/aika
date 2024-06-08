import 'package:frontend/data/models/task_model.dart';

class MessageModel {
  final String text;
  final String userID;
  final String messageID;
  final String role;
  final DateTime timestamp;
  final bool hasTasks;
  List<TaskModel>? tasks;

  MessageModel({required this.text, 
        required this.userID,
        required this.messageID, required this.role,
        required this.timestamp, this.hasTasks=false, this.tasks});
  
  factory MessageModel.fromJson(Map<String, dynamic> json) {
    return MessageModel(
      text: json['text'], 
      userID:json['userId'], 
      messageID: json['messageId'], 
      role: json['role'], 
      timestamp: json['timestamp'],
      hasTasks: json['hasTasks'] ?? false,
      tasks: json['tasks'] != null 
        ? List<TaskModel>.from(json['tasks'].map(
          (task) => TaskModel.fromJson(task)),
      ) : null);
  }

  Map<String, dynamic> toJson() {
    return {
      'text': text,
      'userId': userID,
      'messageId': messageID,
      'timestamp': timestamp.toIso8601String(),
      'role' : role,
      'hasTasks' : hasTasks,
      'tasks' : tasks?.map((task) => task.toJson()).toList(),
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