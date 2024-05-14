import 'package:flutter/material.dart';
import 'package:frontend/german_chat.dart';

class HomePage extends StatelessWidget {
  static const Color accentColor = Color.fromRGBO(224, 71, 23, 1);
  static const Color sandColor = Color.fromRGBO(238, 229, 222, 1);

  /// pushes GermanChatPage to a Naviagtor stack if the button "Deutsch" is pressed
  void _navigateToGermanChat(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => GermanChatPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Dynamically calculate padding and sizes based on screen size
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.01; // 1% of screen width
    double buttonWidth = screenSize.width * 0.82; // 80% of screen width
    double buttonHeight = screenSize.height * 0.07; // 80% of screen width
    double imageDimension = screenSize.width * 0.75; // 75% for square image container

    final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
      backgroundColor: sandColor,
      padding: EdgeInsets.symmetric(vertical: 5, horizontal: padding),
      fixedSize: Size(buttonWidth, buttonHeight),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(5),
      ),
    );

    final TextStyle buttonTextStyle = TextStyle(
      fontFamily: 'SFMono',
      fontSize: screenSize.width * 0.07, // Scale font size based on screen width
      fontWeight: FontWeight.bold,
      color: accentColor,
    );

    const TextStyle styleTitleAIKA = TextStyle(
      color: sandColor,
      fontFamily: 'SFMono',
      height: 1.1,
      fontSize: 70, // Consider scaling this too if necessary
      fontWeight: FontWeight.bold,
    );

    return Scaffold(
      backgroundColor: accentColor,
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Align(
                alignment: Alignment.centerLeft,
                child: Container(
                  padding: EdgeInsets.only(left: padding * 10, top: 45, bottom: screenSize.height*0.05),
                  child: const Text('HALLO, \nICH BIN',
                    textAlign: TextAlign.left,
                    style: styleTitleAIKA,
                  ),
                ),
              ),
              Center(
                child: Container(
                  width: imageDimension,
                  height: imageDimension,
                  decoration: const BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/images/aika.png'),
                      fit: BoxFit.contain,
                    ),
                  ),
                ),
              ),
              SizedBox(height: screenSize.height * 0.05), // Use screen height for consistency
              ElevatedButton(
                style: buttonStyle,
                onPressed: () => _navigateToGermanChat(context),
                child: Text('DEUTSCH!', style: buttonTextStyle),
              ),
              SizedBox(height: screenSize.height * 0.03),
              ElevatedButton(
                style: buttonStyle,
                onPressed: () {
                  print("pressed Recht");
                },
                child: Text('RECHT & ALLTAG', style: buttonTextStyle),
              ),
            ],
          ),
        ),
      ),
    );
  }
}