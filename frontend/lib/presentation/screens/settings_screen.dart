import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/language_bloc.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';
class SettingsScreen extends StatelessWidget {
  
  
  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.03;

    return Scaffold(
      backgroundColor: AppStyles.sandColor,
      appBar: SimpleAppBar(
                text: AppLocalizations.of(context).translate('settings')),
      body: Center(
        child: _buildSettingList(context, padding),
      ),
    );
  }

  Widget _buildSettingList(BuildContext context, double padding) {
    return Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              _buildLanguageSelector(context, padding)
            ],
          );
  }

  Widget _buildLanguageSelector(BuildContext context, double padding) {
    return Container(
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
                    style: AppStyles.settingstextStyle,
                  ),
                  LanguageDropdown(),
                ],
              ),
            );
  }
}

class LanguageDropdown extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    final languageBloc = BlocProvider.of<LanguageBloc>(context);
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.03;

    return BlocBuilder<LanguageBloc, LanguageState>(
      builder: (context, state) => _buildDropdownButton(context, state, padding, languageBloc),
    );
  }

  Widget _buildDropdownButton(BuildContext context, LanguageState state, double padding, LanguageBloc languageBloc) {
    return Container(
        padding: EdgeInsets.only(left: padding),
        decoration: BoxDecoration(
          color: AppStyles.accentColor,
          borderRadius: BorderRadius.circular(3),
          border: Border.all(color: AppStyles.sandColor, width: 2),
        ),
        child: DropdownButton<Locale>(
          dropdownColor: AppStyles.darkColor,
          value: state.locale,
          items: _buildDropdownMenuItems(),
          onChanged: (Locale? newLocale) {
            if (newLocale != null) {
              languageBloc.add(LanguageChanged(newLocale));
            }
          },
        ),
      );
  }

  List<DropdownMenuItem<Locale>> _buildDropdownMenuItems() {
    return const [
            DropdownMenuItem(
              value: Locale('en'),
              alignment: Alignment.center,
              child: Text('English', style: AppStyles.settingsOptionsTextStyle),
            ),
            DropdownMenuItem(
              value: Locale('de'),
              alignment: Alignment.center,
              child: Text('German', style: AppStyles.settingsOptionsTextStyle),
            ),
            DropdownMenuItem(
              value: Locale('ru'),
              alignment: Alignment.center,
              child: Text('Russian', style: AppStyles.settingsOptionsTextStyle),
            ),
            DropdownMenuItem(
              value: Locale('tr'),
              alignment: Alignment.center,
              child: Text('Turkish', style: AppStyles.settingsOptionsTextStyle),
            ),
          ];
  }
}
