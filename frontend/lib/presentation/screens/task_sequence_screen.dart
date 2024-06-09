import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
import 'package:frontend/presentation/widgets/task_buttons_widgets.dart';
import 'package:frontend/presentation/widgets/task_widget.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';

class TaskSequenceScreen extends StatefulWidget {
  final List<Task> tasks;
  final int initialIndex;

  TaskSequenceScreen({required this.tasks, this.initialIndex = 0});

  @override
  _TaskSequenceScreenState createState() => _TaskSequenceScreenState();
}

class _TaskSequenceScreenState extends State<TaskSequenceScreen> {
  late PageController _pageController;
  int _currentIndex;

  _TaskSequenceScreenState() : _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
    _pageController = PageController(initialPage: _currentIndex);
    BlocProvider.of<TaskBloc>(context).add(InitializeTasksEvent(widget.tasks));
  }

  void _onNext() {
    final taskBloc = BlocProvider.of<TaskBloc>(context);
    if (_currentIndex < widget.tasks.length - 1) {
      setState(() {
        _currentIndex++;
      });
      _pageController.nextPage(
        duration: Duration(milliseconds: 300),
        curve: Curves.ease,
      );
    } else {
      Navigator.pop(context);
    }
  }

  void _onBack() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
      });
      _pageController.previousPage(
        duration: Duration(milliseconds: 300),
        curve: Curves.ease,
      );
    } else {
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppLocalizations.of(context).translate('tasks')),
      ),
      backgroundColor: AppStyles.sandColor,
      body: BlocListener<TaskBloc, TaskState>(
        listener: (context, state) {
          if (state is TaskSubmissionSuccess) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Would you like to do the next lesson?')),
            );
          } else if (state is TaskSubmissionFailure) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Failed to submit answers: ${state.error}')),
            );
          }
        },
        child: PageView.builder(
          controller: _pageController,
          itemCount: widget.tasks.length,
          onPageChanged: (index) {
            setState(() {
              _currentIndex = index;
            });
          },
          itemBuilder: (context, index) {
            return TaskWidget(task: widget.tasks[index]);
          },
        ),
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 30),
        child: TaskButtonGroup(
          onBack: _onBack,
          onNext: _onNext,
        ),
      ),
    );
  }
}