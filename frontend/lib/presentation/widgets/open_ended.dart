import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
import 'package:frontend/presentation/widgets/multiple_choice.dart';
import 'package:frontend/styles/app_styles.dart';
class OpenQuestionTask extends StatelessWidget {
  final Task task;

  OpenQuestionTask({required this.task});

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
              Container(
                decoration: const BoxDecoration(color: Colors.white),
                child: OpenQuestionInput(task: task),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class OpenQuestionInput extends StatefulWidget {
  final Task task;

  OpenQuestionInput({required this.task});

  @override
  _OpenQuestionInputState createState() => _OpenQuestionInputState();
}

class _OpenQuestionInputState extends State<OpenQuestionInput> {
  final TextEditingController _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    _controller.text = widget.task.userAnswers.isNotEmpty ? widget.task.userAnswers[0] : '';
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _controller,
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        hintText: 'Type your answer here...',
      ),
      maxLines: 3,
      onChanged: (value) {
        setState(() {
          widget.task.userAnswers = [value];
          widget.task.completed = value.isNotEmpty;
          context.read<TaskBloc>().add(UpdateTaskAnswerEvent([value]));
        });
      },
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}