import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/task_widget/models/task.dart';
import 'package:frontend/task_widget/multiple_choice.dart';
class OpenQuestionTask extends StatelessWidget {
  final Task task;

  OpenQuestionTask({required this.task});

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    return Scaffold(
      backgroundColor: AppStyles.sandColor,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(unitW*5),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              TaskQuestionText(task.question),
              SizedBox(height: unitH*3),
              Container(
                decoration: const BoxDecoration(color: Colors.white),
                child: OpenQuestionInput(),
              ),
              SizedBox(height: unitH),
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
      decoration: const InputDecoration(
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
