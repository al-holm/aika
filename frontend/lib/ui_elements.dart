import 'package:flutter/material.dart';

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
