import 'package:flutter/material.dart';
import 'package:frontend/z_legacy/shared/styles/app_styles.dart';
class MessageButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const MessageButton({
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
      //fixedSize: Size(width, height),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(3),
      ),
    );

    return Expanded(
      child: ElevatedButton(
      style: buttonStyle,
      onPressed: onPressed,
      child: Text(text, style: AppStyles.buttonTextStyle(fontSize, Colors.white)),
      )
    );
  }
}