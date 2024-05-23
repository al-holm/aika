import 'package:flutter/material.dart';
import 'package:frontend/homepage/home_page.dart';
import 'package:frontend/utils/app_localization.dart';
import 'package:frontend/utils/language_provider.dart';
import 'package:provider/provider.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => LanguageProvider(),
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final languageProvider = Provider.of<LanguageProvider>(context);
    return MaterialApp(
      title: 'AIKA',
      theme: ThemeData(
        visualDensity: VisualDensity.adaptivePlatformDensity, // scaling - VisualDensity that is adaptive based on the current platform 
      ),
      locale: languageProvider.locale,
      supportedLocales: const [
        Locale('en', ''),
        Locale('de', ''),
        Locale('ru', ''),
        Locale('tr', ''),
      ],
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      debugShowCheckedModeBanner: false,
      home: HomePage()
    );
  }
}
