import 'package:flutter/material.dart';

/// The function `appBarAIKA` creates a custom AppBar with a title "AIKA" and a back button that
/// navigates to the previous page.
/// 
/// Parameters
/// ----------
/// context : BuildContext
/// 	The `context` parameter in the `appBarAIKA` function is of type `BuildContext`. It represents the
/// location of a widget within the widget tree. The `BuildContext` is used to access information about
/// the location in the widget tree and to interact with the framework. In this case, the
/// 
/// Returns
/// -------
/// 	An AppBar widget with a title "AIKA", a custom background color, and a leading IconButton with an
/// arrow back icon.
AppBar appBarAIKA(BuildContext context) { 
  return AppBar(
    backgroundColor: const Color.fromRGBO(20, 16, 16, 1),
    title: const Text("AIKA", style:TextStyle(color: Colors.white)),
    leading: IconButton(
      icon: const Icon(Icons.arrow_back, color: Colors.white,),
      onPressed: () {
        Navigator.of(context).pop(); // this takes you back to the previous page
      },
    )
    );
}
