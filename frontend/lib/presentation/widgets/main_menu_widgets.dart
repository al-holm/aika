import 'package:flutter/material.dart';
import 'package:frontend/styles/app_styles.dart';

class MainMenuButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;

  const MainMenuButton({
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

class MainMenuSettingButton extends StatelessWidget {
  final VoidCallback onPressed;

  const MainMenuSettingButton({
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

class MainMenuTitleText extends StatelessWidget {
  final double leftPadding;
  final double topPadding;
  final double bottomPadding;

  const MainMenuTitleText({
    Key? key,
    required this.leftPadding,
    required this.topPadding,
    required this.bottomPadding,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        padding: EdgeInsets.only(
          left: leftPadding,
          top: topPadding,
          bottom: bottomPadding,
        ),
        child: const Text(
          'HALLO, \nICH BIN',
          textAlign: TextAlign.left,
          style: AppStyles.mainMenuTitleTextStyle,
        ),
      ),
    );
  }
}

class MainMenuImageContainer extends StatelessWidget {
  final double dimension;

  const MainMenuImageContainer({
    Key? key,
    required this.dimension,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: dimension,
      height: dimension,
      decoration: const BoxDecoration(
        image: DecorationImage(
          image: AssetImage('assets/images/aika.png'),
          fit: BoxFit.contain,
        ),
      ),
    );
  }
}
