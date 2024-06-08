import 'package:flutter/material.dart';
/// returns a widget app bar with the app title and back button
/// after pressing on back button the current widget will be popped from the Navigator stack 
/// and the user sees previous widget
AppBar appBarAIKA(BuildContext context, String title) { 
  return AppBar(
    backgroundColor: const Color.fromRGBO(20, 16, 16, 1),
    title: Text(title, style: const TextStyle(color: Colors.white)),
    leading: IconButton(
      icon: const Icon(Icons.arrow_back, color: Colors.white,),
      onPressed: () {
        /// `Navigator.of(context).pop();` is a method call in Flutter that is used to pop (remove) the
        /// current route from the navigation stack. In simpler terms, it navigates back to the previous
        /// page or screen in the app.
        Navigator.of(context).pop(); 
      },
    )
    );
}
