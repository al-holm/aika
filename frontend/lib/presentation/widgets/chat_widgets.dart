import 'package:flutter/material.dart';
import 'package:frontend/styles/app_styles.dart';

class BotAvatar extends StatelessWidget {
  const BotAvatar({
    Key? key,
    required this.unitW,
  }) : super(key: key);

  final double unitW;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: unitW * 15,
      height: unitW * 15,
      decoration: const BoxDecoration(
        image: DecorationImage(
          image: AssetImage('assets/images/bot_avatar.png'),
          fit: BoxFit.scaleDown,
        ),
        shape: BoxShape.circle,
      ),
    );
  }
}


class LoadingIndicator extends StatelessWidget {
  const LoadingIndicator({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return  Container(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: const Center(
        child: CircularProgressIndicator(color: AppStyles.accentColor,)
    )
    );
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
      fixedSize: Size(screenSize.width*0.2, screenSize.height*0.06),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(3),
      ),
    );

    return  Container(
      margin: EdgeInsets.symmetric(horizontal: padding*8),
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