import 'package:flutter/material.dart';
import 'package:frontend/home_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AIKA',
      theme: ThemeData(
        fontFamily: 'SF Pro',
        primarySwatch: Colors.deepOrange, 
        visualDensity: VisualDensity.adaptivePlatformDensity, // scaling - VisualDensity that is adaptive based on the current platform 
      ),
      debugShowCheckedModeBanner: false,
      home: HomePage()
    );
  }
}

// read more about TextEditingController, Expanded, Divider, ListView, ListTile
