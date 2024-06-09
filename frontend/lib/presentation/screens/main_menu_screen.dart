import 'package:flutter/material.dart';
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
        child: Center(
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
        ),
      ),
    );
  }
  
  _navigateToSettings(BuildContext context) {
    Navigator.pushNamed(context, '/settings');
  }
  
  _navigateToGermanChat(BuildContext context) {
    Navigator.pushNamed(context, '/german');
  }
  
  _navigateToLawChat(BuildContext context) {
    Navigator.pushNamed(context, '/law');
  }
}
