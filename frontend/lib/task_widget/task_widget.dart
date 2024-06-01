import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/task_widget/dummy_tasks.dart';
import 'package:frontend/task_widget/fill_gaps.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/multiple_choice.dart';
import 'package:frontend/task_widget/open_ended.dart';
import 'package:frontend/task_widget/widgets/buttons.dart';
import 'package:frontend/utils/app_localization.dart';

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

class TaskSequenceScreen extends StatefulWidget {
  @override
  _TaskSequenceScreenState createState() => _TaskSequenceScreenState();
}
class _TaskSequenceScreenState extends State<TaskSequenceScreen> {
  final PageController _pageController = PageController();
  final List<Task> tasks = [multipleChoiceTask, fillInTheGapTask, openEndedTask];
  int _currentIndex = 0;

  void _onNext() {
    if (_currentIndex < tasks.length - 1) {
      setState(() {
        _currentIndex++;
      });
      _pageController.nextPage(
        duration: Duration(milliseconds: 300),
        curve: Curves.ease,
      );
    } else {
      Navigator.pop(context);  
    }
  }

  void _onBack() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
      });
      _pageController.previousPage(
        duration: Duration(milliseconds: 300),
        curve: Curves.ease,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBarAIKA(context, AppLocalizations.of(context).translate('tasks')),
      backgroundColor: AppStyles.sandColor,
      body: PageView.builder(
        controller: _pageController,
        itemCount: tasks.length,
        onPageChanged: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        itemBuilder: (context, index) {
          return TaskWidget(task: tasks[index]);
        },
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 30),
        child: TaskButtonGroup(
          onBack: _currentIndex > 0 ? _onBack : null,
           onNext: _onNext,
        ),
      ),
    );
  }
}
