import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
import 'package:frontend/presentation/screens/task_sequence_screen.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/presentation/widgets/chat_widgets.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';


class GermanChatScreen extends StatelessWidget {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final String chatID = 'german';

  @override
  Widget build(BuildContext context) {
    final chatBloc = BlocProvider.of<ChatBloc>(context);
    final taskBloc = BlocProvider.of<TaskBloc>(context);
    String newLessonText = AppLocalizations.of(context).translate('new_lesson');

    return SafeArea(
      child: Scaffold(
        backgroundColor: AppStyles.sandColor,
        appBar: GermanChatAppBar(),
        body: Column(
          children: <Widget>[
            Expanded(child: _buildChatInteractionArea(chatBloc, taskBloc, newLessonText)),
            const SizedBox(height: 15,),
            const Divider(height: 1, color: AppStyles.darkColor,),
            _buildTextInput(chatBloc),
          ],
        ),
      ),
    );
  }

  Widget _buildChatInteractionArea(ChatBloc chatBloc, TaskBloc taskBloc, String newLessonText) {
    return MultiBlocListener(
          listeners: [
            BlocListener<TaskBloc, TaskState>(
              listener: (context, state) {
                if (state is TaskSubmissionSuccess) {
                  chatBloc.add(ProposeLessonEvent(true, chatID));
                }
              },
            ),
          ],
          child: BlocBuilder<ChatBloc, ChatState>(
            builder: (context, state) => _chatStateBuilder(state, chatBloc, taskBloc, newLessonText),
                  ),
          );
    }

  Widget _chatStateBuilder(ChatState state, ChatBloc chatBloc, TaskBloc taskBloc, String newLessonText) {
    if (state is ChatInitial) {
      chatBloc.add(InitializeChatEvent(chatID));
      return const LoadingIndicator();
    } else if (state is ChatLoading) {
      return _buildLoadingView(state);
    } else if (state is ChatLoaded) {
      return _buildLoadedView(state, chatBloc, newLessonText);
    } else if (state is LessonLoaded) {
      return _buildLessonView(state, chatBloc);
    } else if (state is TaskLoaded) {
      return _buildTaskView(state, taskBloc, chatBloc);
    } else if (state is ChatError) {
      return _buildErrorView(state, chatBloc);
    } else {
      return const Center(child: Text("Keine Nachrichten vorhanden."));
    }
  }

  Widget _buildLoadingView(ChatLoading state) {
    return ListView(
          controller: _scrollController,
          children: [
            _buildMessageList(state.messages),
            const LoadingIndicator(),
          ],
          );
  }

  Widget _buildLoadedView(ChatLoaded state, ChatBloc chatBloc, String newLessonText) {
    return ListView(
          controller: _scrollController,
          children: [
            _buildMessageList(state.messages),
            if (state.offerLesson)
              ChatButton(
                text: newLessonText,
                onPressed: () {
                  chatBloc.add(FetchLessonEvent(chatID));
                },
              ),
          ],
        );
  }

  Widget _buildLessonView(LessonLoaded state, ChatBloc chatBloc) {
    chatBloc.add(FetchTaskEvent(chatID));
    return ListView(
      controller: _scrollController,
      children: [
        _buildMessageList(state.messages),
      ],
    );
  }

  Widget _buildTaskView(TaskLoaded state, TaskBloc taskBloc, ChatBloc chatBloc) {
    taskBloc.add(InitializeTasksEvent(state.tasks));
    return ListView(
      controller: _scrollController,
      children: [
        _buildMessageList(state.messages),
        BlocBuilder<TaskBloc, TaskState>(
          builder: (context, taskState) {
            if (taskState is TaskSubmissionSuccess) {
              return const SizedBox();
            } else {
              return ChatButton(
                text: AppLocalizations.of(context).translate('tasks'),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => TaskSequenceScreen(tasks: state.tasks),
                    ),
                  );
                },
              );
            }
          },
        ),
      ],
    );
  }

  Widget _buildMessageList(List<Message> messages) {
    return ListView.builder(
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      itemCount: messages.length,
      itemBuilder: (context, index) {
        final message = messages[index];
        return MessageTile(
          content: message.text,
          role: message.role,
        );
      },
    );
  }

  Widget _buildErrorView(ChatError state, ChatBloc chatBloc) {
    return ListView(
      controller: _scrollController,
      children: [
        _buildMessageList(state.messages),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            children: [
              const Text(
                "Etwas ist fehlgeschlagen. Erneut generieren.",
                style: TextStyle(color: Colors.grey),
              ),
              IconButton(
                icon: const Icon(Icons.refresh, color: Colors.grey),
                onPressed: () {
                  chatBloc.add(state.lastEvent!);
                },
              ),
            ],
          ),
        ),
      ]
    );
  }

  Widget _buildTextInput(ChatBloc chatBloc) {
    return ChatTextInput(
              controller: _controller,
              handleSubmitted: () {
                final content = _controller.text;
                if (content.isNotEmpty) {
                  chatBloc.add(SendMessageEvent(chatID, content));
                  _controller.clear();
                }
              },
            );
  }
}