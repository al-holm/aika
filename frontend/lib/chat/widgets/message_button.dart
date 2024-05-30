import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
class TaskControl extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const TaskControl({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width * 0.3;
    double height = screenSize.height * 0.05;
    double fontSize = screenSize.width * 0.06;
    double padding = screenSize.width * 0.01;

    final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
      backgroundColor: AppStyles.accentColor,
      padding: EdgeInsets.symmetric(vertical: padding, horizontal: padding),
      fixedSize: Size(width, height),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(3),
      ),
    );

    return ElevatedButton(
      style: buttonStyle,
      onPressed: onPressed,
      child: Text(text, style: AppStyles.buttonTextStyle(fontSize, Colors.white)),
    );
  }
}