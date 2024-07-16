import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/screens/german_chat_screen.dart';
import 'package:frontend/presentation/screens/law_chat_screen.dart';
import 'package:frontend/presentation/widgets/text_field_widgets.dart';
import 'package:frontend/styles/app_styles.dart';

class AuthentificationScreen extends StatefulWidget {
  const AuthentificationScreen({super.key});

  @override
  State<AuthentificationScreen> createState() => _AuthentificationScreenState();
}

class _AuthentificationScreenState extends State<AuthentificationScreen> {
  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double imageDimension = screenSize.width * 0.76;
    double padding = screenSize.width * 0.01;

    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: AppStyles.accentColor,
      body: SafeArea(
          child: _buildScreenContent(
              context, screenSize, imageDimension, padding)),
    );
  }

  Widget _buildScreenContent(BuildContext context, Size screenSize,
      double imageDimension, double padding) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Container(
              padding: EdgeInsets.only(top: screenSize.height * 0.03),
              child: const Text(
                'Welcome!',
                textAlign: TextAlign.left,
                style: AppStyles.mainMenuTitleTextStyle,
              )),
          SizedBox(height: screenSize.height * 0.04),
          TextFieldAuth(),
          SizedBox(height: screenSize.height * 0.04),
          Center(
            child: Container(
              width: imageDimension,
              height: imageDimension,
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage('assets/images/flower.png'),
                  fit: BoxFit.contain,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  _navigateToSettings(BuildContext context) {
    Navigator.pushNamed(context, '/settings');
  }

  _navigateToGermanChat(BuildContext context) {
    _navigateToChat(context, 'german');
  }

  _navigateToLawChat(BuildContext context) {
    _navigateToChat(context, 'law');
  }

  _navigateToChat(BuildContext context, String chatID) {
    final chatBloc = BlocProvider.of<ChatBloc>(context);
    chatBloc.add(ClearChatEvent(chatID));
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) =>
            chatID == 'german' ? GermanChatScreen() : LawChatScreen(),
      ),
    );
  }
}
