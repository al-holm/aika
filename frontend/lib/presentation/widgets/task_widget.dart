import 'package:flutter/material.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/widgets/fill_gaps.dart';
import 'package:frontend/presentation/widgets/multiple_choice.dart';
import 'package:frontend/presentation/widgets/open_ended.dart';
class TaskWidget extends StatelessWidget {
  final Task task;

  TaskWidget({required this.task});

  @override
  Widget build(BuildContext context) {
    switch (task.type) {
      case TaskType.multipleChoice:
        return MultipleChoiceTask(task: task);
      case TaskType.fillTheGaps:
        return FillInTheGapTask(task: task);
      case TaskType.openQuestion:
        return OpenQuestionTask(task: task);
      default:
        return Center(child: Text('Unknown task type'));
    }
  }
}