enum TaskType{
  multipleChoice, 
  fillTheGaps, openQuestion
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