import 'package:flutter/material.dart';
import 'package:frontend/z_legacy/shared/styles/app_styles.dart';
class TaskStyles{
  static const TextStyle questionTextStyle = TextStyle(
      color: AppStyles.darkColor,
      fontFamily: 'SFMono',
      height: 1.1,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    );
  static const TextStyle optionTextStyle = TextStyle(
      color: AppStyles.darkColor,
      fontFamily: 'SFMono',
      height: 3,
      fontSize: 18,
    );
}