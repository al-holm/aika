import 'package:flutter/material.dart';
import 'package:frontend/germanchat/models/message.dart';
import 'package:frontend/germanchat/widgets/loading_dots.dart';
import 'package:frontend/germanchat/widgets/message_tile.dart';
import 'package:frontend/germanchat/widgets/text_input.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'services/chat_service.dart';
import 'services/metadata_service.dart';

class GermanChatPage extends StatefulWidget {
  @override
  _GermanChatState createState() => _GermanChatState();
}

class _GermanChatState extends State<GermanChatPage> {
  late String _userId;
  final TextEditingController _controller = TextEditingController();
  List<Message> _messages = [];
  bool isLoading = false;
  // 'http://10.0.2.2:3000/ - for Android emulation
  final ChatService chatService = ChatService(apiUrl: 'http://192.168.178.149:3000/german-chat/message/'); //http://127.0.0.1 for ios
  final MetadataService metadataService = MetadataService();

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    _userId = await metadataService.initUserId();
    _initMessages();
  }

  Future<void> _initMessages() async {
    String initString = "Hallo, ich bin AIKA! Ich kann dir helfen, Deutsch zu lernen.\n\nWillst du mit dem neuen Untericht starten oder hast Fragen?";
    Message initMessage = chatService.buildMessage(initString, 'bot', _userId, 'init');
    setState(() {
      _messages.add(initMessage);
    });
  }

  Future<void> _handleSubmitted(String text) async {
    if (text == '') return;
    _controller.clear();

    Message userMessage = chatService.buildMessage(text, 'user', _userId);

    setState(() {
      _messages.add(userMessage);
      isLoading = true;
    });

    Message? botMessage = await chatService.sendMessage(userMessage);

    if (botMessage != null) {
      setState(() {
        _messages.add(botMessage);
        isLoading = false;
      });
    } else {
      print("Failed to get response from server.");
    }
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    return SafeArea(
      child: Scaffold(
        backgroundColor: AppStyles.sandColor,
        appBar: appBarAIKA(context, 'AIKA Chat'),
        body: Column(
          children: <Widget>[
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.only(top: unitH*2, left: unitW, right: unitW*2, bottom:unitH*2),
                reverse: true,
                itemBuilder: (_, int index) => MessageTile(message: _messages.reversed.toList()[index]),
                itemCount: _messages.length,
              ),
            ),
            if (isLoading)
              Padding(
                padding: EdgeInsets.symmetric(vertical: unitH*2),
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