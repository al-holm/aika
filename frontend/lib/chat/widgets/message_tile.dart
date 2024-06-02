import 'package:flutter/material.dart';
import 'package:frontend/chat/chat.dart';
import 'package:frontend/chat/models/message.dart';
import 'package:frontend/chat/widgets/message_button.dart';
import 'package:frontend/task_widget/dummy_tasks.dart';
import 'package:frontend/task_widget/task_widget.dart';
import 'package:frontend/utils/app_localization.dart';


class MessageTile extends StatelessWidget {
  final Message message;

  const MessageTile({required this.message});

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    bool isBot = message.role == 'bot';
    double radius = unitW*2;
    var borderRadius = isBot
        ? BorderRadius.only(
            topLeft: Radius.circular(radius),
            topRight: Radius.circular(radius),
            bottomLeft: const Radius.circular(0),
            bottomRight: Radius.circular(radius),
          )
        : BorderRadius.only(
            topLeft: Radius.circular(radius),
            topRight: Radius.circular(radius),
            bottomLeft: Radius.circular(radius),
            bottomRight: const Radius.circular(0),
          );

    return Row(
      mainAxisAlignment: isBot ? MainAxisAlignment.start : MainAxisAlignment.end,
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        if (isBot)
          Container(
            width: unitW*15,
            height: unitW*15,
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage('assets/images/bot_avatar.png'),
                fit: BoxFit.scaleDown,
              ),
              shape: BoxShape.circle,
            ),
          ),
        Container(
          margin: EdgeInsets.symmetric(horizontal: unitW, vertical: unitH),
          padding: EdgeInsets.symmetric(horizontal: unitW *1.5, vertical: unitH),
          constraints: BoxConstraints(maxWidth: screenSize.width * 0.7),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: borderRadius,
            border: Border.all(color: Colors.black, width: 1.5),
          ),
          child: Text(
            message.text,
            style: const TextStyle(fontFamily: 'SFMono', fontSize: 17),
          ),
        ),
      ],
    );
  }
}

class GermanMessageTile extends MessageTile {
  const GermanMessageTile({required Message message}) : super(message: message);

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    bool isBot = message.role == 'bot';
    double radius = unitW * 2;
    var borderRadius = isBot
        ? BorderRadius.only(
            topLeft: Radius.circular(radius),
            topRight: Radius.circular(radius),
            bottomLeft: const Radius.circular(0),
            bottomRight: Radius.circular(radius),
          )
        : BorderRadius.only(
            topLeft: Radius.circular(radius),
            topRight: Radius.circular(radius),
            bottomLeft: Radius.circular(radius),
            bottomRight: const Radius.circular(0),
          );

    return Column(
      children: [
        Row(
          mainAxisAlignment: isBot ? MainAxisAlignment.start : MainAxisAlignment.end,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            if (isBot)
              Container(
                width: unitW * 15,
                height: unitW * 15,
                decoration: const BoxDecoration(
                  image: DecorationImage(
                    image: AssetImage('assets/images/bot_avatar.png'),
                    fit: BoxFit.scaleDown,
                  ),
                  shape: BoxShape.circle,
                ),
              ),
            Container(
              margin: EdgeInsets.symmetric(horizontal: unitW, vertical: unitH),
              padding: EdgeInsets.symmetric(horizontal: unitW * 1.5, vertical: unitH),
              constraints: BoxConstraints(maxWidth: screenSize.width * 0.7),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: borderRadius,
                border: Border.all(color: Colors.black, width: 1.5),
              ),
              child: Text(
                message.text,
                style: const TextStyle(fontFamily: 'SFMono', fontSize: 17),
              ),
            ),
          ],
        ),
        if (isBot && message.gotTasks)
          Container(
            alignment: Alignment.center,
            child: MessageButton(
              text: AppLocalizations.of(context).translate('tasks'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => TaskSequenceScreen(
                      tasks: [multipleChoiceTask, fillInTheGapTask, openEndedTask], // Pass your tasks here
                      initialIndex: 0, // Start from the first task
                    ),
                  ),
                );
              },
            ),
          ),
        if (isBot && message.messageID == 'init')
          Container(
            alignment: Alignment.center,
            child: MessageButton(
              text: AppLocalizations.of(context).translate('new_lesson'),
              onPressed: () {
                final chatState = context.findAncestorStateOfType<ChatState<ChatPage>>();
                chatState?.handleNewLesson();
              },
            ),
          ),
      ],
    );
  }
}