import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
import 'package:frontend/presentation/screens/task_sequence_screen.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/presentation/widgets/chat_widgets.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';


class GermanChatScreen extends StatelessWidget {
  final TextEditingController _controller = TextEditingController();
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
            Expanded(
              child: BlocBuilder<ChatBloc, ChatState>(
                builder: (context, state) {
                  if (state is ChatInitial) {
                    chatBloc.add(InitializeChatEvent(chatID));
                    return const LoadingIndicator();
                  } else if (state is ChatLoading) {
                    return const LoadingIndicator();
                  } else if (state is ChatLoaded) {
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        Expanded(
                          child: ListView.builder(
                            itemCount: state.messages.length,
                            itemBuilder: (context, index) {
                              final message = state.messages[index];
                              return MessageTile(
                                content: message.text,
                                role: message.role,
                              );
                            },
                          ),
                        ),
                        if (state.hasLesson)
                          ChatButton(
                            text: newLessonText,
                            onPressed: () {
                              chatBloc.add(FetchLessonEvent(chatID));
                            },
                          ),
                          const SizedBox(height: 15,),
                      ],
                    );
                  } else if (state is LessonLoaded) {
                    taskBloc.add(InitializeTasksEvent(state.lesson.tasks!));
                    return Column(
                      children: [
                        Expanded(
                          child: ListView.builder(
                            itemCount: state.messages.length,
                            itemBuilder: (context, index) {
                              final message = state.messages[index];
                              return MessageTile(
                                content: message.text,
                                role: message.role,
                              );
                            },
                          ),
                        ),
                        MessageTile(
                          content: state.lesson.text,
                          role: state.lesson.role,
                        ),
                        ChatButton(
                          text: AppLocalizations.of(context).translate('tasks'),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => TaskSequenceScreen(tasks: state.lesson.tasks!),
                              ),
                            );
                          },
                        ),
                      ],
                    );
                  } else if (state is ChatError) {
                    return Center(child: Text(state.message));
                  } else {
                    return const Center(child: Text("Keine Nachrichten vorhanden."));
                  }
                },
              ),
            ),
            const Divider(height: 1),
            ChatTextInput(
              controller: _controller,
              handleSubmitted: () {
                final content = _controller.text;
                if (content.isNotEmpty) {
                  chatBloc.add(SendMessageEvent(chatID, content));
                  _controller.clear();
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}