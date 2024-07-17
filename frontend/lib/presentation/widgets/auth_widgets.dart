import 'package:flutter/material.dart';
import 'package:frontend/styles/app_styles.dart';

class TextFieldAuthWidget extends StatelessWidget {
  const TextFieldAuthWidget(
      {super.key,
      required TextEditingController controller,
      required String label})
      : _controller = controller,
        _label = label;

  final TextEditingController _controller;
  final String _label;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _controller,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: _label,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
        ),
        filled: true,
        fillColor: AppStyles.sandColor,
      ),
    );
  }
}

class WelcomeTitleWidget extends StatelessWidget {
  const WelcomeTitleWidget({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    return Container(
        padding: EdgeInsets.only(top: screenSize.height * 0.03),
        child: const Text(
          'Welcome!',
          textAlign: TextAlign.left,
          style: AppStyles.mainMenuTitleTextStyle,
        ));
  }
}

class CheckBoxWidget extends StatefulWidget {
  const CheckBoxWidget({
    super.key,
    required this.isSignUp,
    required this.onChanged,
  });

  final bool isSignUp;
  final Function(bool?) onChanged;

  @override
  _CheckBoxWidgetState createState() => _CheckBoxWidgetState();
}

class _CheckBoxWidgetState extends State<CheckBoxWidget> {
  late bool _isSignUp;

  @override
  void initState() {
    super.initState();
    _isSignUp = widget.isSignUp;
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Checkbox(
          side: const BorderSide(width: 2, color: AppStyles.sandColor),
          checkColor: AppStyles.accentColor,
          activeColor: AppStyles.sandColor,
          value: _isSignUp,
          onChanged: (value) {
            setState(() {
              _isSignUp = value!;
            });
            widget.onChanged(value);
          },
        ),
        Text(
          'Sign up',
          style: AppStyles.buttonTextStyle(16, AppStyles.sandColor),
        )
      ],
    );
  }
}

class AuthImageContainerWidget extends StatelessWidget {
  const AuthImageContainerWidget({super.key, required double imageDimension})
      : _imageDimension = imageDimension;

  final double _imageDimension;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: _imageDimension,
        height: _imageDimension,
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/images/flower.png'),
            fit: BoxFit.contain,
          ),
        ),
      ),
    );
  }
}
