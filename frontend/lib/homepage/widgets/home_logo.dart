import 'package:flutter/material.dart';

class RabbitImageContainer extends StatelessWidget {
  final double dimension;

  const RabbitImageContainer({
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