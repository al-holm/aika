import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';

class HomeStyles {
  static TextStyle buttonTextStyle(double fontSize) {
    return TextStyle(
      fontFamily: 'SFMono',
      fontSize: fontSize,
      fontWeight: FontWeight.bold,
      color: AppStyles.accentColor,
    );
  }

  static const TextStyle titleTextStyle = TextStyle(
    color: AppStyles.sandColor,
    fontFamily: 'SFMono',
    height: 1.1,
    fontSize: 70,
    fontWeight: FontWeight.bold,
  );

}