import 'package:flutter/material.dart';

class AppStyles {
  static const Color accentColor = Color.fromRGBO(224, 71, 23, 1);
  static const Color sandColor = Color.fromRGBO(238, 229, 222, 1);
  static const Color darkColor =  Color.fromRGBO(20, 16, 16, 1);
  static TextStyle buttonTextStyle(double fontSize, Color color) {
    return TextStyle(
      fontFamily: 'SFMono',
      fontSize: fontSize,
      fontWeight: FontWeight.bold,
      color: color,
    );
  }
}