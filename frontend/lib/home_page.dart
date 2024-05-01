
import 'package:flutter/material.dart';
import 'package:frontend/german_chat.dart';

class HomePage extends StatelessWidget {
  static const Color accentColor = Color.fromRGBO(224, 71, 23, 1);
  static const Color sandColor =  Color.fromRGBO(238, 229, 222, 1);
  final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
    backgroundColor: sandColor,
    padding: const EdgeInsets.symmetric(vertical: 5),
    fixedSize: const Size(320, 55),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(5),
    )
  );

  final TextStyle buttonTextStyle = const TextStyle(fontFamily: 'SFMono',
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: accentColor);

  static const TextStyle styleTitleAIKA = TextStyle(
                            color: sandColor,
                            fontFamily: 'SFMono',
                            height: 1.1,
                            fontSize: 70,
                            fontWeight: FontWeight.bold);

  void _navigateToGermanChat(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => GermanChatPage())
    );
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      backgroundColor: accentColor,
      body: SafeArea( // ensures padding from system components (notches, bars etc.)
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Align(
                alignment: Alignment.centerLeft,
                child: Container(
                  padding: const EdgeInsets.only(left: 20, top: 40, bottom: 10),
                  child: 
                        const Text('HALLO, \nICH BIN', 
                          textAlign: TextAlign.left,
                          style: styleTitleAIKA,
                        ) 
                  )
              ),
              Center(
                child: Container(
                  width: 300, // Set the width of the container
                  height: 300, // Set the height of the container
                  decoration: const BoxDecoration(
                    image:  DecorationImage(
                      image: AssetImage('assets/images/aika.png'),
                      fit: BoxFit.contain, // Covers the container space
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 40,), // to adjust space between components
              ElevatedButton(
                style: buttonStyle,
                onPressed: () => _navigateToGermanChat(context), 
                child: 
                  Text('DEUTSCH!',
                    style: buttonTextStyle,
                  ),
                ),
              const SizedBox(height: 15,), // to adjust space between components
              ElevatedButton(
                style: buttonStyle,
                onPressed: () {
                  print("pressed Recht");
                }, 
                child: 
                  Text('RECHT & ALLTAG',
                    style: buttonTextStyle,
                  ),
                ),
          ],)
        ),
      )
    );
  }
}

