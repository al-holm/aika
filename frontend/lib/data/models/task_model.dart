import 'package:frontend/domain/entities/task.dart';

class TaskModel {
  final TaskType type;
  final String question;
  final List<List<String>> answerOptions;
  final List<String> solutions;

  TaskModel({
    required this.type,
    required this.question,
    required this.answerOptions,
    required this.solutions,
  });
  
  factory TaskModel.fromJson(Map<String, dynamic> json) {
    TaskType type = TaskTypeExtension.fromString(json['type']);
    dynamic jsonSolutions = json['solution'];
    if (type == TaskType.fillTheGaps) {
      jsonSolutions = jsonSolutions[0];
    }
    return TaskModel(
      type: type,
      question:  json['question'],
      answerOptions: (json['answer_options'] as List<dynamic>).map((e) => List<String>.from(e).toSet().toList()).toList(), // remov duplicates if exists
      solutions: List<String>.from(jsonSolutions),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'type': type.index,
      'question': question,
      'answerOptions': answerOptions.map((e) => e.toList()).toList(),
      'solutions': solutions,
    };
  }
}