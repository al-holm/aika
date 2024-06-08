import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:frontend/z_legacy/chat/models/message.dart';
import 'package:frontend/z_legacy/chat/services/metadata_service.dart';
import 'package:frontend/z_legacy/chat/widgets/loading_dots.dart';
import 'package:frontend/z_legacy/chat/widgets/text_input.dart';
import 'package:frontend/z_legacy/shared/styles/app_styles.dart';
import 'package:frontend/z_legacy/shared/ui_elements.dart';
import 'package:frontend/z_legacy/task_widget/dummy_tasks.dart';

abstract class ChatPage extends StatefulWidget {
  final String apiUrl;
  final String initialMessage;
  final String appBarTitle;
  final Widget Function(Message) messageTileBuilder;

  const ChatPage({
    required this.apiUrl, 
    required this.initialMessage, 
    required this.appBarTitle,
    required this.messageTileBuilder,
    });

  @override
  State<ChatPage> createState() => ChatState();

  Future<Message?> sendMessage(Message message);
}

class ChatState<T extends ChatPage> extends State<T> {
  late String _userId;
  final TextEditingController _controller = TextEditingController();
  final List<Message> messages = [];
  bool isLoading = false;
  final MetadataService metadataService = MetadataService();

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    _userId = await initUserId();
    _initMessages();
  }

  Future<String> initUserId() async {
    return metadataService.initUserId();
  }

  Future<void> _initMessages() async {
    Message initMessage = Message(
      text: widget.initialMessage,
      userID: 'bot',
      messageID: 'init',
      role: 'bot',
      timestamp: DateTime.now(),
    );
    setState(() {
      messages.add(initMessage);
    });
  }

  Future<void> _handleSubmitted(String text) async {
    if (text == '') return;
    _controller.clear();

    Message userMessage = Message(
      text: text,
      userID: _userId,
      messageID: MetadataService.generateMessageID(),
      role: 'user',
      timestamp: DateTime.now(),
    );
    setState(() {
      messages.add(userMessage);
      isLoading = true;
    });

    Message? botMessage = await widget.sendMessage(userMessage);

    if (botMessage != null) {
      setState(() {
        messages.add(botMessage);
        isLoading = false;
      });
    } else {
      log("Failed loading message.");
    }
  }

  void handleNewLesson() {
    return;
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    return SafeArea(
      child: Scaffold(
        backgroundColor: AppStyles.sandColor,
        appBar: appBarAIKA(context, widget.appBarTitle),
        body: Column(
          children: <Widget>[
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.only(top: unitH * 2, left: unitW, right: unitW * 2, bottom: unitH * 2),
                reverse: true,
                itemBuilder: (_, int index) => widget.messageTileBuilder(messages.reversed.toList()[index]),
                itemCount: messages.length,
              ),
            ),
            if (isLoading)
              Padding(
                padding: EdgeInsets.symmetric(vertical: unitH * 2),
                child: LoadingIndicator(),
              ),
            const Divider(height: 1),
            TextInput(controller: _controller, handleSubmitted: _handleSubmitted),
          ],
        ),
      ),
    );
  }
}