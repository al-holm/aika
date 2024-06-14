import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
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
        appBar: SimpleAppBar(text: AppLocalizations.of(context).translate('law&daily')),
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
      return Center(child: Text(state.message));
    } else {
      return const Center(child: Text("Keine Nachrichten vorhanden."));
    }
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