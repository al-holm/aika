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
    return TaskModel(
      type: TaskType.values[json['type']],
      question: json['question'],
      answerOptions: List<List<String>>.from(
        json['answerOptions'].map((e) => List<String>.from(e)),
      ),
      solutions: List<String>.from(json['solutions']),
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