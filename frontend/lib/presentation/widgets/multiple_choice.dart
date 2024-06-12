import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
import 'package:frontend/styles/app_styles.dart';

class MultipleChoiceTask extends StatelessWidget {
  final Task task;

  MultipleChoiceTask({required this.task});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppStyles.sandColor,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TaskQuestionText(task.question),
              SizedBox(height: 16),
              MultipleChoiceOptions(
                options: task.answerOptions,
                userAnswers: task.userAnswers,
                onSelected: (selected) {
                  context.read<TaskBloc>().add(UpdateTaskAnswerEvent([selected]));
                },
              ),
            ],
          ),
        ),
      ),
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
              style: AppStyles.taskOptionTextStyle,
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

class TaskQuestionText extends StatelessWidget {
  final String question;

  TaskQuestionText(this.question);

  @override
  Widget build(BuildContext context) {
    return Text(
      question,
      style: AppStyles.taskQuestionTextStyle,
      textAlign: TextAlign.left,
    );
  }
}
