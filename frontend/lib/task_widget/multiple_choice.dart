import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/styles/task_styles.dart';
import 'package:frontend/task_widget/widgets/buttons.dart';

class MultipleChoiceTask extends StatefulWidget {
  final Task task;

  MultipleChoiceTask({required this.task});
  @override
  _MultipleChoiceTaskState createState() => _MultipleChoiceTaskState();
}

class _MultipleChoiceTaskState extends State<MultipleChoiceTask> {
  int? _selectedOption;


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBarAIKA(context, "Tasks"),
      backgroundColor: AppStyles.sandColor,
      body: SafeArea(
      child: Container(
        color: AppStyles.sandColor,
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(15.0),
            child: Text(
              widget.task.question,
              style: TaskStyles.questionTextStyle,
              textAlign: TextAlign.center,
            ),
          ),
           Expanded(
            child: ListView.builder(
              itemCount: widget.task.answerOptions.length,
              itemBuilder: (context, index) {
                return RadioListTile<int>(
                  title: Text(widget.task.answerOptions[index],
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
          ),
          Padding(
            padding: const EdgeInsets.all(15.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                TaskControlButton(text: 'Back', onPressed: () {
                    // Handle back action
                  },
                ),
                TaskControlButton(text: 'Continue', onPressed: () {
                    // Handle back action
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    )
    )
    );
  }
}