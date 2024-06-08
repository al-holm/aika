import 'package:flutter/material.dart';
import 'package:frontend/z_legacy/homepage/styles/home_pages_styles.dart';
import 'package:frontend/z_legacy/shared/styles/app_styles.dart';

class HomeButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const HomeButton({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width * 0.82;
    double height = screenSize.height * 0.07;
    double fontSize = screenSize.width * 0.07;
    double padding = screenSize.width * 0.01;

    final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
      backgroundColor: AppStyles.sandColor,
      padding: EdgeInsets.symmetric(vertical: padding, horizontal: padding),
      fixedSize: Size(width, height),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(5),
      ),
    );

    return ElevatedButton(
      style: buttonStyle,
      onPressed: onPressed,
      child: Text(text, style: AppStyles.buttonTextStyle(fontSize, AppStyles.accentColor)),
    );
  }
}

class SettingButton extends StatelessWidget {
  final VoidCallback onPressed;

  const SettingButton({
    super.key,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double iconSize = screenSize.width * 0.1;


    return IconButton(
                onPressed: onPressed, 
                icon:  Icon(
                  Icons.settings_sharp,
                  color: AppStyles.sandColor,
                  size: iconSize,
                  ),
    );
  }
}