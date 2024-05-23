import 'package:flutter/material.dart';
import 'package:frontend/settings/styles/settings_styles.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/utils/language_provider.dart';
import 'package:provider/provider.dart';

class LanguageDropdown extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    final languageProvider = Provider.of<LanguageProvider>(context);
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.03;

    return Container(
      padding: EdgeInsets.only(left: padding),
      decoration: BoxDecoration(
                color: AppStyles.accentColor,
                borderRadius: BorderRadius.circular(3),
                border: Border.all(color: AppStyles.sandColor, width: 2),
              ),
      child: DropdownButton<Locale>(
        dropdownColor: AppStyles.darkColor,
        value: languageProvider.locale,
        items: [
          DropdownMenuItem(
            value: const Locale('en'),
            alignment: Alignment.center,
            child: Text('English', style: SettingsStyles.optionsTextStyle),
          ),
          DropdownMenuItem(
            value: const Locale('de'),
            alignment: Alignment.center,
            child: Text('German', style: SettingsStyles.optionsTextStyle),
          ),
          DropdownMenuItem(
            value: const Locale('ru'),
            alignment: Alignment.center,
            child: Text('Russian', style: SettingsStyles.optionsTextStyle),
          ),
          DropdownMenuItem(
            value: const Locale('tr'),
            alignment: Alignment.center,
            child: Text('Turkish', style: SettingsStyles.optionsTextStyle),
          ),
        ],
        onChanged: (Locale? newLocale) {
          if (newLocale != null) {
            languageProvider.setLocale(newLocale);
          }
        },
      ),
    );
  }
}
