import 'package:frontend/domain/entities/task.dart';

class TaskModel {
  final TaskType type;
  final String question;
  final List<List<String>> answerOptions;
  final List<String> solutions;
  final int id;
  final String lessonType;

  TaskModel({
    required this.type,
    required this.question,
    required this.answerOptions,
    required this.solutions,
    required this.id, required this.lessonType
  });
  
  factory TaskModel.fromJson(Map<String, dynamic> json, int id, String lessonType) {
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
      id: id,
      lessonType: lessonType
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