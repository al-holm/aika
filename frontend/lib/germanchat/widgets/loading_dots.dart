import 'package:flutter/material.dart';


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
      duration: const Duration(milliseconds: 1000),
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
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;
    return FadeTransition(
      opacity: _controller.drive(
        CurveTween(curve: Curves.easeInOut),
      ),
      child: Container(
        margin: EdgeInsets.all(unitW),
        width: unitW*2,
        height: unitH*2,
        decoration: const BoxDecoration(
          color: Colors.black,
          shape: BoxShape.circle,
        ),
      ),
    );
  }
}


class LoadingIndicator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.01;
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children:  <Widget>[
        Dot(),
        SizedBox(width: padding*0.5),
        Dot(),
        SizedBox(width: padding*0.5),
        Dot(),
      ],
    );
  }
}