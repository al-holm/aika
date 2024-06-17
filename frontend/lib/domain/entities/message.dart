import 'package:frontend/domain/entities/task.dart';

class Message {
  final String text;
  final String userID;
  final String messageID;
  final String role;
  final DateTime timestamp;
  final bool hasTasks;
  final List<Task>? tasks;

  Message({required this.text, 
        required this.userID,
        required this.messageID, required this.role,
        required this.timestamp,
        this.hasTasks = false,
        this.tasks,});
}

