import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/styles/task_styles.dart';
import 'package:frontend/task_widget/widgets/buttons.dart';
import 'package:frontend/utils/app_localization.dart';
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
          padding: EdgeInsets.all(10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Fill in the gaps:',
                style: TaskStyles.questionTextStyle,
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 16),
              FillInTheGapQuestion(task: task),
              SizedBox(height: 16),
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
  final List<String> selectedAnswers = ['', ''];

  @override
  Widget build(BuildContext context) {
    final parts = widget.task.question.split('__');
    final List<InlineSpan> spans = [];

    for (int i = 0; i < parts.length; i++) {
      spans.add(TextSpan(text: parts[i], style: TaskStyles.optionTextStyle));
      if (i < widget.task.answerOptions!.length) {
        spans.add(WidgetSpan(
          alignment: PlaceholderAlignment.middle,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0),
            child: Transform.translate(
              offset: const Offset(0, -2), // Adjust the offset to lower the dropdown
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
      items: widget.task.answerOptions![index].map((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value, style: TaskStyles.optionTextStyle),
        );
      }).toList(),
      onChanged: (value) {
        setState(() {
          selectedAnswers[index] = value!;
        });
      },
    );
  }
}