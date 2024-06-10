import 'package:flutter/material.dart';
import 'package:frontend/styles/app_styles.dart';

class MessageTile extends StatelessWidget {
  final String content;
  final String role;

  const MessageTile({required this.content, required this.role});

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    bool isBot = role == 'bot';
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
          mainAxisAlignment:
              isBot ? MainAxisAlignment.start : MainAxisAlignment.end,
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
              padding: EdgeInsets.symmetric(
                  horizontal: unitW * 1.5, vertical: unitH),
              constraints: BoxConstraints(maxWidth: screenSize.width * 0.7),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: borderRadius,
                border: Border.all(color: Colors.black, width: 1.5),
              ),
              child: Text(
                content,
                style: AppStyles.messageTextStyle,
                softWrap: true,
              ),
            ),
          ],
        ),
      ]
    );
  }
}



class LoadingIndicator extends StatelessWidget {
  const LoadingIndicator({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return const Center(child: CircularProgressIndicator());
  }
}


class ChatButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const ChatButton({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double fontSize = screenSize.width * 0.06;
    double padding = screenSize.width * 0.01;

    final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
      backgroundColor: AppStyles.accentColor,
      padding: EdgeInsets.symmetric(vertical: padding*1.5, horizontal: padding*3),
      //fixedSize: Size(screenSize.width*0.4, screenSize.height*0.06),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(3),
      ),
    );

    return  Expanded(
      child: ElevatedButton(
        style: buttonStyle,
        onPressed: onPressed,
        child: Text(text, style: AppStyles.buttonTextStyle(fontSize, Colors.white)),
      )
    );
  }
}


class ChatTextInput extends StatelessWidget {
  final TextEditingController controller;
  final Function handleSubmitted;

  const ChatTextInput({required this.controller, required this.handleSubmitted});

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;

    void localHandleSubmitted(String text) {
      handleSubmitted();
      FocusScope.of(context).requestFocus(FocusNode());
    }

    return Container(
      color: AppStyles.sandColor,
      padding: EdgeInsets.only(left: unitW*2, right: unitW*2, top: unitH*2, bottom: unitH*2),
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: Colors.black),
          color: Colors.white,
          borderRadius: BorderRadius.circular(5),
        ),
        child: Row(
          children: <Widget>[
            Expanded(
              child: Padding(
                padding: EdgeInsets.only(left: unitW*3),
                child: TextField(
                  controller: controller,
                  keyboardType: TextInputType.multiline,
                  maxLines: 7,
                  minLines: 1,
                  onSubmitted: localHandleSubmitted,
                  decoration: const InputDecoration.collapsed(hintText: 'Tippen Sie hier...'),
                ),
              ),
            ),
            IconButton(
              onPressed: () => localHandleSubmitted(controller.text),
              icon: const Icon(Icons.send),
            ),
          ],
        ),
      ),
    );
  }
}