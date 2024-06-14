import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/screens/german_chat_screen.dart';
import 'package:frontend/presentation/screens/law_chat_screen.dart';
import 'package:frontend/presentation/widgets/main_menu_widgets.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';
class MainMenuScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double imageDimension = screenSize.width * 0.76;
    double padding = screenSize.width * 0.01;

    return Scaffold(
      backgroundColor: AppStyles.accentColor,
      body: SafeArea(
        child: _buildMenuContent(context, screenSize, imageDimension, padding)
      ),
    );
  }

  Widget _buildMenuContent(BuildContext context, Size screenSize, double imageDimension, double padding) {
    return Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Container(
                alignment: Alignment.topRight,
                padding: EdgeInsets.only(right: padding * 3, top: padding * 2),
                child: MainMenuSettingButton(
                  onPressed: () => _navigateToSettings(context)
                  ),
              ),
              MainMenuTitleText(
                leftPadding: padding * 10,
                topPadding: screenSize.height * 0.00,
                bottomPadding: screenSize.height * 0.03,
              ),
              Center(
                child: MainMenuImageContainer(dimension: imageDimension),
              ),
              SizedBox(height: screenSize.height * 0.05),
              MainMenuButton(
                text: AppLocalizations.of(context).translate('germanChat'),
                onPressed: () => _navigateToGermanChat(context),
              ),
              SizedBox(height: screenSize.height * 0.03),
              MainMenuButton(
                text: AppLocalizations.of(context).translate('law&daily'),
                onPressed: () {
                   _navigateToLawChat(context);
                },
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
        builder: (context) => chatID == 'german' ? GermanChatScreen() : LawChatScreen(),
        ),
    );
  }
}
