import 'dart:convert';
import 'package:frontend/domain/entities/task.dart';
import 'package:http/http.dart' as http;

class TaskDataProvider {
  final String baseUrl;

  TaskDataProvider(this.baseUrl);

  Future<void> submitUserAnswers(List<Task> tasks) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat/submit_answers'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'tasks': tasks.map((task) => {
          'type': task.type.toString().split('.').last,
          'question': task.question,
          'userAnswers': task.userAnswers,
        }).toList(),
      }),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to submit answers');
    }
  }
}

// Thought : adjust TaskModel to submit the answer using the model!