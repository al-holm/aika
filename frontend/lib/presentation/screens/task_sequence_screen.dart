import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/blocs/task_bloc/task_bloc.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/presentation/widgets/chat_widgets.dart';
import 'package:frontend/presentation/widgets/task_buttons_widgets.dart';
import 'package:frontend/presentation/widgets/task_widget.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';

class TaskSequenceScreen extends StatelessWidget {
  final List<Task> tasks;

  TaskSequenceScreen({required this.tasks});

  @override
  Widget build(BuildContext context) {
    final taskBloc = BlocProvider.of<TaskBloc>(context);
    taskBloc.add(InitializeTasksEvent(tasks));

    return BlocListener<TaskBloc, TaskState>(
      listener: (context, state) {
        if (state is TaskSubmissionSuccess) {
          Navigator.pop(context);
        }
      },
      child: BlocBuilder<TaskBloc, TaskState>(
          builder: (context, state) => state is TaskInProgress
              ? _buildTaskInProgress(context, state, taskBloc)
              : _buildLoadingScreen(context)),
    );
  }

  Widget _buildTaskInProgress(
      BuildContext context, TaskInProgress state, TaskBloc taskBloc) {
    final currentTask = state.tasks[state.currentTaskIndex];

    return Scaffold(
      appBar:
          SimpleAppBar(text: AppLocalizations.of(context).translate('tasks')),
      backgroundColor: AppStyles.sandColor,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(child: TaskWidget(task: currentTask)),
            _buildTaskControlButtons(context, state, taskBloc, currentTask)
          ],
        ),
      ),
    );
  }

  Widget _buildLoadingScreen(BuildContext context) {
    return Scaffold(
        appBar:
            SimpleAppBar(text: AppLocalizations.of(context).translate('tasks')),
        body: const LoadingIndicator());
  }

  Widget _buildTaskControlButtons(BuildContext context, TaskInProgress state,
      TaskBloc taskBloc, Task currentTask) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        if (state.currentTaskIndex > 0)
          _buildBackButton(context, state, taskBloc),
        if (state.currentTaskIndex < state.tasks.length - 1)
          _buildContinueButton(context, state, taskBloc, currentTask),
        if (state.currentTaskIndex == state.tasks.length - 1)
          _buildSubmitButton(context, state, taskBloc),
      ],
    );
  }

  Widget _buildBackButton(
      BuildContext context, TaskInProgress state, TaskBloc taskBloc) {
    return TaskControlButton(
      onPressed: () {
        FocusScope.of(context).unfocus();
        taskBloc.add(CompleteTaskEvent(state.currentTaskIndex,
            state.tasks[state.currentTaskIndex].userAnswers, false));
      },
      text: AppLocalizations.of(context).translate('back'),
    );
  }

  Widget _buildContinueButton(BuildContext context, TaskInProgress state,
      TaskBloc taskBloc, Task currentTask) {
    return TaskControlButton(
      onPressed: () {
        taskBloc.add(CompleteTaskEvent(
            state.currentTaskIndex,
            currentTask.userAnswers,
            true // going next - true, going back - false
            ));
      },
      text: AppLocalizations.of(context).translate('continue'),
    );
  }

  Widget _buildSubmitButton(
      BuildContext context, TaskInProgress state, TaskBloc taskBloc) {
    return TaskControlButton(
      onPressed: () {
        taskBloc.add(SubmitTasksEvent(state.tasks));
      },
      text: AppLocalizations.of(context).translate('submit'),
    );
  }
}
