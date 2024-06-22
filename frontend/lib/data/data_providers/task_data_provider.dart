import 'dart:convert';
import 'package:frontend/domain/entities/task.dart';
import 'package:http/http.dart' as http;

class TaskDataProvider {
  final String baseUrl;

  TaskDataProvider(this.baseUrl);

  Future<void> submitUserAnswers(List<Task> tasks) async {
    final data = tasks.map((task) => {
          'id': task.id,
          'lessonType': task.lessonType,
          'type': task.type.toString().split('.').last,
          'question': task.question,
          'userAnswers': task.userAnswers,
          'solutions': task.solutions,
        }).toList();
    final response = await http.post(
      Uri.parse('$baseUrl/chat/submit_answers'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );
    print(response);
    if (response.statusCode != 201) {
      throw Exception('Failed to submit answers');
    }
  }
}