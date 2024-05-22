import 'package:flutter/material.dart';

Widget _buildLoadingIndicator() {
  return Row(
    mainAxisAlignment: MainAxisAlignment.center,
    children: <Widget>[
      Dot(),
      SizedBox(width: 4),
      Dot(),
      SizedBox(width: 4),
      Dot(),
    ],
  );
}

class Dot extends StatefulWidget {
  @override
  _DotState createState() => _DotState();
}

class _DotState extends State<Dot> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 800),
      vsync: this,
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _controller.drive(
        CurveTween(curve: Curves.easeInOut),
      ),
      child: Container(
        width: 8,
        height: 8,
        decoration: BoxDecoration(
          color: Colors.black,
          shape: BoxShape.circle,
        ),
      ),
    );
  }
}
