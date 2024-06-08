import 'dart:ffi';

import 'package:frontend/chat/services/metadata_service.dart';
import 'package:frontend/task_widget/models/task.dart';
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

    if (response.statusCode == 201) {
      final responseData = jsonDecode(response.body)['message'];
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

  Future<List> getLesson() async {
    final uri = Uri.parse(apiUrl);
    String newSegment = 'lesson';
    List<String> segments = List<String>.from(uri.pathSegments);
  
    if (segments.isNotEmpty) {
      segments[segments.length - 2] = newSegment;
    }

    Uri url = uri.replace(pathSegments: segments);
    final response = await http.post(url);
    if (response.statusCode == 201) {
      final responseData = jsonDecode(response.body);
      print(responseData);
      final lesson_text = responseData['text'];
      final tasksS = responseData['tasks'];
      List<Task> tasks = [];
      for (var i = 0; i < tasksS.length; i++) {
        var taskElement = tasksS[i];
        String type = taskElement["type"];
        Map<String, TaskType> qtMap = {
          "single-choice": TaskType.multipleChoice,
          "gaps": TaskType.fillTheGaps,
          "open": TaskType.openQuestion
        };
        TaskType taskType = qtMap[type] as TaskType; 

        var answer_dynamic = taskElement["answer_options"].map((dynamic e) => List<String>.from(e)).toList();
        List<List<String>> answer_options = [];
        for (var i = 0; i < answer_dynamic.length; i++) {
          var el = answer_dynamic[i];
          List<String> list_s = List<String>.from(el);
          answer_options.add(list_s);
        }
        var question = taskElement['question'];
        var sol = taskElement['solution'];
        List<String> solution = [];
        if (taskType != TaskType.fillTheGaps) {
          solution = List<String>.from(sol);
        } else {
          solution = List<String>.from(sol[0]);
        }
        Task task = Task(
          taskType,
          question,
          answer_options,
          solution
        );
        tasks.add(task);
      }
      return [lesson_text, tasks];
    } else{
      print(response.statusCode);
      
    }
    return [];
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
