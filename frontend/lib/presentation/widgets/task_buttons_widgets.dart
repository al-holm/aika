import 'package:flutter/material.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';
class TaskControlButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const TaskControlButton({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width * 0.4;
    double height = screenSize.height * 0.06;
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




class TaskButtonGroup extends StatelessWidget {
  final VoidCallback? onBack;
  final VoidCallback? onNext;

  TaskButtonGroup({this.onBack, this.onNext});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
       TaskControlButton(
          text: AppLocalizations.of(context).translate('back'),
          onPressed: onBack ?? () {},  
        ),
        TaskControlButton(
          text: AppLocalizations.of(context).translate('continue'),
          onPressed: onNext ?? () {},  
        ),
      ],
    );
  }
}
