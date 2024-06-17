enum TaskType{
  multipleChoice, 
  fillTheGaps, openQuestion
}

extension TaskTypeExtension on TaskType {
  static TaskType fromString(String type) {
    switch (type) {
      case 'single-choice':
        return TaskType.multipleChoice;
      case 'gaps':
        return TaskType.fillTheGaps;
      case 'open':
        return TaskType.openQuestion;
      default:
        throw ArgumentError('Invalid task type');
    }
  }
}

class Task {
  final TaskType type;
  final String question;
  final List<List<String>> answerOptions;
  final List<String> solutions;
  List<String> userAnswers = [];
  bool completed = false; 

  Task({
    required this.type, required this.question, 
    required this.answerOptions, required this.solutions
    });
}