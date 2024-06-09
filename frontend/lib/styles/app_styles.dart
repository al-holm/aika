import 'package:flutter/material.dart';

class AppStyles {
  static const Color accentColor = Color.fromRGBO(224, 71, 23, 1);
  static const Color sandColor = Color.fromRGBO(238, 229, 222, 1);
  static const Color darkColor = Color.fromRGBO(20, 16, 16, 1);

  static TextStyle buttonTextStyle(double fontSize, Color color) {
    return TextStyle(
      fontFamily: 'SFMono',
      fontSize: fontSize,
      fontWeight: FontWeight.bold,
      color: color,
    );
  }

  static const TextStyle settingsOptionsTextStyle = TextStyle(
    color: sandColor,
    fontFamily: 'SFMono',
    height: 1.1,
    fontSize: 16,
    fontWeight: FontWeight.bold,
  );

  static const TextStyle settingstextStyle = TextStyle(
    color: sandColor,
    fontFamily: 'SFMono',
    height: 1.1,
    fontSize: 20,
    fontWeight: FontWeight.bold,
  );

  static const TextStyle mainMenuTitleTextStyle = TextStyle(
      color: sandColor,
      fontFamily: 'SFMono',
      height: 1.1,
      fontSize: 70,
      fontWeight: FontWeight.bold,
    );


  static const TextStyle taskQuestionTextStyle = TextStyle(
      color: darkColor,
      fontFamily: 'SFMono',
      height: 1.1,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    );

  static const TextStyle taskOptionTextStyle = TextStyle(
      color: darkColor,
      fontFamily: 'SFMono',
      height: 1.1,
      fontSize: 18,
    );
  static const TextStyle messageTextStyle = TextStyle(
    fontFamily: 'SFMono', fontSize: 17
    );
}