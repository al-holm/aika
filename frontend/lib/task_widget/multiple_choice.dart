import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/styles/task_styles.dart';
import 'package:frontend/task_widget/widgets/buttons.dart';
import 'package:frontend/utils/app_localization.dart';
class MultipleChoiceTask extends StatelessWidget {
  final Task task;

  MultipleChoiceTask({required this.task});

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    return Scaffold(
      backgroundColor: AppStyles.sandColor,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              TaskQuestionText(task.question),
              SizedBox(height: 16),
              MultipleChoiceOptions(task.answerOptions),
              SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}

class TaskQuestionText extends StatelessWidget {
  final String question;

  TaskQuestionText(this.question);

  @override
  Widget build(BuildContext context) {
    return Text(
      question,
      style: TaskStyles.questionTextStyle,
      textAlign: TextAlign.left,
    );
  }
}

class MultipleChoiceOptions extends StatefulWidget {
  final List<List<String>> options;

  MultipleChoiceOptions(this.options);

  @override
  _MultipleChoiceOptionsState createState() => _MultipleChoiceOptionsState();
}

class _MultipleChoiceOptionsState extends State<MultipleChoiceOptions> {
  int? _selectedOption;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        itemCount: widget.options[0].length,
        itemBuilder: (context, index) {
          return RadioListTile<int>(
            title: Text(
              widget.options[0][index],
              style: TaskStyles.optionTextStyle,
            ),
            value: index,
            groupValue: _selectedOption,
            activeColor: AppStyles.accentColor,
            onChanged: (int? value) {
              setState(() {
                _selectedOption = value;
              });
            },
          );
        },
      ),
    );
  }
}
