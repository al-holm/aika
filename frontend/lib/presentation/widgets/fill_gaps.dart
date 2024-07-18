import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/blocs/task_bloc/task_bloc.dart';
import 'package:frontend/styles/app_styles.dart';

class FillInTheGapTask extends StatelessWidget {
  final Task task;

  FillInTheGapTask({required this.task});

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
              const Text(
                'Füllen Sie die Lücken basierend auf dem Text:',
                style: AppStyles.taskQuestionTextStyle,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              FillInTheGapQuestion(task: task),
            ],
          ),
        ),
      ),
    );
  }
}

class FillInTheGapQuestion extends StatefulWidget {
  final Task task;

  FillInTheGapQuestion({required this.task});

  @override
  _FillInTheGapQuestionState createState() => _FillInTheGapQuestionState();
}

class _FillInTheGapQuestionState extends State<FillInTheGapQuestion> {
  late List<String> selectedAnswers;

  @override
  void initState() {
    super.initState();
    selectedAnswers = List<String>.from(widget.task.userAnswers.isNotEmpty
        ? widget.task.userAnswers
        : List.filled(widget.task.answerOptions.length, ''));
  }

  @override
  Widget build(BuildContext context) {
    final parts = widget.task.question.split('__');
    final List<InlineSpan> spans = [];

    for (int i = 0; i < parts.length; i++) {
      spans.add(TextSpan(text: parts[i], style: AppStyles.taskOptionTextStyle));
      if (i < widget.task.answerOptions.length) {
        spans.add(WidgetSpan(
          alignment: PlaceholderAlignment.middle,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Transform.translate(
              offset: const Offset(0, -8.0 / 1.5),
              child: buildDropdown(i),
            ),
          ),
        ));
      }
    }

    return RichText(
      text: TextSpan(
        children: spans,
      ),
    );
  }

  Widget buildDropdown(int index) {
    return DropdownButton<String>(
      value: selectedAnswers[index].isEmpty ? null : selectedAnswers[index],
      hint: const Text(''),
      items: widget.task.answerOptions[index].map((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value, style: AppStyles.taskOptionTextStyle),
        );
      }).toList(),
      onChanged: (value) {
        setState(() {
          selectedAnswers[index] = value!;
          widget.task.userAnswers = selectedAnswers;
          widget.task.completed =
              selectedAnswers.every((answer) => answer.isNotEmpty);
          context.read<TaskBloc>().add(UpdateTaskAnswerEvent(selectedAnswers));
        });
      },
    );
  }
}
