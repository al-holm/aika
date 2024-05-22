import 'package:flutter/material.dart';
import 'package:frontend/germanchat/german_chat.dart';
import 'package:frontend/homepage/widgets/home_buttons.dart';
import 'package:frontend/homepage/widgets/home_logo.dart';
import 'package:frontend/homepage/widgets/home_title.dart';
import 'package:frontend/settings/settings_page.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/utils/app_localization.dart';

class HomePage extends StatelessWidget {
  void _navigateToGermanChat(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => GermanChatPage()),
    );
  }

  void _navigateToSettings(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => SettingsPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double imageDimension = screenSize.width * 0.76;
    double padding = screenSize.width * 0.01;

    return Scaffold(
      backgroundColor: AppStyles.accentColor,
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Container(
                alignment: Alignment.topRight,
                padding: EdgeInsets.only(right: padding * 3, top: padding * 2),
                child: SettingButton(
                  onPressed: () => _navigateToSettings(context)
                  ),
              ),
              HomeTitleText(
                leftPadding: padding * 10,
                topPadding: screenSize.height * 0.00,
                bottomPadding: screenSize.height * 0.03,
              ),
              Center(
                child: RabbitImageContainer(dimension: imageDimension),
              ),
              SizedBox(height: screenSize.height * 0.05),
              HomeButton(
                text: AppLocalizations.of(context).translate('germanChat'),
                onPressed: () => _navigateToGermanChat(context),
              ),
              SizedBox(height: screenSize.height * 0.03),
              HomeButton(
                text: AppLocalizations.of(context).translate('law&daily'),
                onPressed: () {
                  print("pressed Recht");
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
