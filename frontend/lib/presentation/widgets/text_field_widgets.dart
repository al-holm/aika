import 'package:flutter/material.dart';
import 'package:frontend/presentation/widgets/main_menu_widgets.dart';
import 'package:frontend/styles/app_styles.dart';

class TextFieldAuth extends StatefulWidget {
  const TextFieldAuth({super.key});

  @override
  State<TextFieldAuth> createState() => _TextFieldAuthState();
}

class _TextFieldAuthState extends State<TextFieldAuth> {
  late TextEditingController _usernameController;
  late TextEditingController _passwordController;
  bool _isSignUp = false;

  @override
  void initState() {
    super.initState();
    _usernameController = TextEditingController();
    _passwordController = TextEditingController();
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void handleSubmitted() {
    final username = _usernameController.text;
    final password = _passwordController.text;
    if (username.isNotEmpty && password.isNotEmpty) {
      _usernameController.clear();
      _passwordController.clear();
      // here send values username, password & isSignUp to server
    }
    FocusScope.of(context).requestFocus(FocusNode());
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    return Container(
      padding: EdgeInsets.symmetric(horizontal: screenSize.height * 0.02),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          TextField(
            controller: _usernameController,
            keyboardType: TextInputType.text,
            decoration: InputDecoration(
              labelText: 'Username',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(5),
              ),
              filled: true,
              fillColor: AppStyles.sandColor,
            ),
          ),
          SizedBox(height: screenSize.height * 0.01),
          TextField(
            controller: _passwordController,
            keyboardType: TextInputType.text,
            decoration: InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(5),
              ),
              filled: true,
              fillColor: AppStyles.sandColor,
            ),
          ),
          SizedBox(height: screenSize.height * 0.01),
          Container(
              child: Row(
            children: [
              Checkbox(
                side: const BorderSide(width: 2, color: AppStyles.sandColor),
                checkColor: AppStyles.accentColor,
                activeColor: AppStyles.sandColor,
                value: _isSignUp,
                onChanged: (bool? value) {
                  setState(() {
                    _isSignUp = value ?? false;
                  });
                },
              ),
              Text(
                'Sign up',
                style: AppStyles.buttonTextStyle(16, AppStyles.sandColor),
              )
            ],
          )),
          SizedBox(height: screenSize.height * 0.01),
          MainMenuButton(text: 'Submit', onPressed: () => handleSubmitted()),
        ],
      ),
    );
  }
}
