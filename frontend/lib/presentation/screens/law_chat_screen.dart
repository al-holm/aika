import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/presentation/widgets/chat_widgets.dart';
import 'package:frontend/presentation/widgets/message_tile.dart';
import 'package:frontend/styles/app_styles.dart';

class LawChatScreen extends StatelessWidget {
  final TextEditingController _controller = TextEditingController();
  final String chatID = 'law';

  @override
  Widget build(BuildContext context) {
    final chatBloc = BlocProvider.of<ChatBloc>(context);

    return SafeArea(
      child: Scaffold(
        backgroundColor: AppStyles.sandColor,
        appBar: LawChatAppBar(),
        body: Column(
          children: <Widget>[
            Expanded(child: _buildChatContent(chatBloc)),
            const Divider(height: 1),
            _buildTextInput(chatBloc),
          ],
        ),
      ),
    );
  }

  Widget _buildChatContent(ChatBloc chatBloc) {
    return BlocBuilder<ChatBloc, ChatState>(
          builder: (context, state) => _buildChatState(state, chatBloc)
        );
  }

  Widget _buildChatState(ChatState state, ChatBloc chatBloc) {
    if (state is ChatInitial) {
      chatBloc.add(InitializeChatEvent(chatID));
      return const LoadingIndicator();
    } else if (state is ChatLoading) {
      return _buildLoadingView(state);
    } else if (state is ChatLoaded) {
      return _buildLoadedView(state);
    } else if (state is ChatError) {
      return _buildErrorView(state, chatBloc);
    } else {
      return const Center(child: Text("Keine Nachrichten vorhanden."));
    }
  }

  Widget _buildErrorView(ChatError state, ChatBloc chatBloc) {
    return ListView(
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

  Widget _buildLoadingView(ChatLoading state) {
    return ListView(
        children: [
          _buildMessageList(state.messages),
          const LoadingIndicator()
        ]
      );
  }

  Widget _buildLoadedView(ChatLoaded state) {
    return ListView(
        children: [
          _buildMessageList(state.messages),
          const SizedBox(height: 15,),
        ],
      );
  }

  Widget _buildMessageList(List<Message> messages) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: messages.length,
      itemBuilder: (context, index) {
        final message = messages[index];
        return MessageTile(
          content: message.text,
          role: message.role,
          messageType: message.messageType,
        );
      },
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