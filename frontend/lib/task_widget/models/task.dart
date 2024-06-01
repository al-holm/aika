enum TaskType{
  multipleChoice, fillTheGaps, openQuestion
}

class Task {
  TaskType type;
  String question;
  List<List<String>> answerOptions;
  List<String> solutions;
  late List<String> userAnswers;
  bool completed = false; 

  Task(this.type, this.question, this.answerOptions, this.solutions);

  
}