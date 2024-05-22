import 'package:flutter/material.dart';
import 'package:frontend/settings/styles/settings_styles.dart';
import 'package:frontend/settings/widgets/language_dropdown.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/utils/app_localization.dart';

class SettingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.03;

    return Scaffold(
      appBar: appBarAIKA(context, 
        AppLocalizations.of(context).translate('settings')
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Container(
              padding: EdgeInsets.all(padding),
              margin: EdgeInsets.all(padding*1),
              decoration: BoxDecoration(
                color: AppStyles.accentColor,
                borderRadius: BorderRadius.circular(4),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    AppLocalizations.of(context).translate('selectLanguage'),
                    style: SettingsStyles.textStyle,
                  ),
                  LanguageDropdown(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
