import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
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

    return BlocListener<TaskBloc, TaskState>(
      listener: (context, state) {
        if (state is TaskSubmissionSuccess) {
          Navigator.pop(context);
        }
      },
      child: BlocBuilder<TaskBloc, TaskState>(
        builder: (context, state) {
          if (state is TaskInProgress) {
            final currentTask = state.tasks[state.currentTaskIndex];
            return Scaffold(
              appBar: SimpleAppBar(
                text: AppLocalizations.of(context).translate('tasks')),
              backgroundColor: AppStyles.sandColor,
              body: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Expanded(child: TaskWidget(task: currentTask)),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        if (state.currentTaskIndex > 0)
                          TaskControlButton(
                            onPressed: () {
                              if (currentTask.completed )
                              {  
                              taskBloc.add(CompleteTaskEvent(
                              state.currentTaskIndex,
                              state.tasks[state.currentTaskIndex].userAnswers,
                              false
                                ));
                              }
                            },
                            text: AppLocalizations.of(context).translate('back'),
                          ),
                        if (state.currentTaskIndex < state.tasks.length - 1)
                          TaskControlButton(
                            onPressed: () {
                              if (currentTask.completed )
                              {  taskBloc.add(CompleteTaskEvent(
                                state.currentTaskIndex,
                                currentTask.userAnswers,
                                true // going next - true, goint back false
                                ));
                              }
                            },
                            text: AppLocalizations.of(context).translate('continue'),
                          ),
                        if (state.currentTaskIndex == state.tasks.length - 1)
                          TaskControlButton(
                            onPressed: () {
                              if (currentTask.completed )
                              {  
                                taskBloc.add(SubmitTasksEvent(state.tasks));
                              }
                            },
                            text: AppLocalizations.of(context).translate('submit'),
                          ),
                      ],
                    ),
                  ],
                ),
              ),
            );
          } else {
            return Scaffold(
              appBar: SimpleAppBar(
                text: AppLocalizations.of(context).translate('tasks')),
              body: const LoadingIndicator()
            ); 
        }
        }
      ),
    );
  }
}