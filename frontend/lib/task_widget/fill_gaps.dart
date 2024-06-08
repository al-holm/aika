import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/styles/task_styles.dart';

class FillInTheGapTask extends StatelessWidget {
  final Task task;

  FillInTheGapTask({required this.task});

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
              const Text(
                'Füllen Sie die Lücken basierend auf dem Text:',
                style: TaskStyles.questionTextStyle,
                textAlign: TextAlign.center,
              ),
              SizedBox(height: unitH * 2),
              FillInTheGapQuestion(task: task),
              SizedBox(height: unitH),
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
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    final parts = widget.task.question.split('__');
    final List<InlineSpan> spans = [];

    for (int i = 0; i < parts.length; i++) {
      spans.add(TextSpan(text: parts[i], style: TaskStyles.optionTextStyle));
      if (i < widget.task.answerOptions.length) {
        spans.add(WidgetSpan(
          alignment: PlaceholderAlignment.middle,
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: unitW),
            child: Transform.translate(
              offset: Offset(0, -unitW / 1.5),
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
      hint: Text(''),
      items: widget.task.answerOptions[index].map((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value, style: TaskStyles.optionTextStyle),
        );
      }).toList(),
      onChanged: (value) {
        setState(() {
          selectedAnswers[index] = value!;
          widget.task.userAnswers = selectedAnswers;
        });
      },
    );
  }
}