import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/styles/task_styles.dart';

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
          padding: EdgeInsets.all(unitW * 5),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              TaskQuestionText(task.question),
              SizedBox(height: unitH * 2),
              MultipleChoiceOptions(
                options: task.answerOptions,
                userAnswers: task.userAnswers,
                onSelected: (selected) {
                  task.userAnswers = [selected];
                },
              ),
              SizedBox(height: unitH),
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
  final List<String> userAnswers;
  final ValueChanged<String> onSelected;

  MultipleChoiceOptions({
    required this.options,
    required this.userAnswers,
    required this.onSelected,
  });

  @override
  _MultipleChoiceOptionsState createState() => _MultipleChoiceOptionsState();
}

class _MultipleChoiceOptionsState extends State<MultipleChoiceOptions> {
  int? _selectedOption;

  @override
  void initState() {
    super.initState();
    if (widget.userAnswers.isNotEmpty) {
      _selectedOption = widget.options[0].indexOf(widget.userAnswers[0]);
    }
  }

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
              if (value != null) {
                setState(() {
                  _selectedOption = value;
                });
                widget.onSelected(widget.options[0][value]);
              }
            },
          );
        },
      ),
    );
  }
}