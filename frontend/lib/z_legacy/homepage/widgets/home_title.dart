import 'package:flutter/material.dart';
import 'package:frontend/z_legacy/homepage/styles/home_pages_styles.dart';

class HomeTitleText extends StatelessWidget {
  final double leftPadding;
  final double topPadding;
  final double bottomPadding;

  const HomeTitleText({
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
          style: HomeStyles.titleTextStyle,
        ),
      ),
    );
  }
}
