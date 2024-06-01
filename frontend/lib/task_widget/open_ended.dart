import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/multiple_choice.dart';
import 'package:frontend/task_widget/styles/task_styles.dart';
import 'package:frontend/task_widget/widgets/buttons.dart';
import 'package:frontend/utils/app_localization.dart';
class OpenQuestionTask extends StatelessWidget {
  final Task task;

  OpenQuestionTask({required this.task});

  @override
  Widget build(BuildContext context) {
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
              Container(
                decoration: BoxDecoration(color: Colors.white),
                child: OpenQuestionInput(),
              ),
              SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}

class OpenQuestionInput extends StatefulWidget {
  @override
  _OpenQuestionInputState createState() => _OpenQuestionInputState();
}

class _OpenQuestionInputState extends State<OpenQuestionInput> {
  final TextEditingController openQuestionController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: openQuestionController,
      decoration: InputDecoration(
        border: OutlineInputBorder(),
        hintText: 'Type your answer here...',
      ),
      maxLines: 3,
    );
  }

  @override
  void dispose() {
    openQuestionController.dispose();
    super.dispose();
  }
}
