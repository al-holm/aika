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


class LawChatScreen extends StatelessWidget {
  final TextEditingController _controller = TextEditingController();
  final String chatID = 'law';

  @override
  Widget build(BuildContext context) {
    final chatBloc = BlocProvider.of<ChatBloc>(context);

    return SafeArea(
      child: Scaffold(
        backgroundColor: AppStyles.sandColor,
        appBar: GermanChatAppBar(),
        body: Column(
          children: <Widget>[
            Expanded(
              child: MultiBlocListener(
                child: BlocBuilder<ChatBloc, ChatState>(
                  builder: (context, state) {
                    if (state is ChatInitial) {
                      chatBloc.add(InitializeChatEvent(chatID));
                      return const LoadingIndicator();
                    } else if (state is ChatLoading) {
                      return ListView(
                        children: [
                          _buildMessageList(state.messages),
                          LoadingIndicator()
                        ]
                      );
                    } else if (state is ChatLoaded) {
                      return ListView(
                        children: [
                          _buildMessageList(state.messages),
                          const SizedBox(height: 15,),
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
}