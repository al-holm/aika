import 'package:frontend/task_widget/models/task.dart';

class TaskIterator implements Iterator {
  List<Task?>? tasks;
  @override
  Task? current;

  TaskIterator(this.tasks) {
    current = tasks?[0];
  }

  @override
  bool moveNext() {
    int? index = tasks?.indexOf(current);
    if (index != -1 && index != null) {
      index = index + 1; 
      if (index < tasks!.length) {
        current = tasks![index];
        return true;
      }
    }
    return false;
  }
  
}