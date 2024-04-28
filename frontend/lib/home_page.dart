
import 'package:flutter/material.dart';
import 'package:frontend/german_chat.dart';

class HomePage extends StatelessWidget {

  final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
    backgroundColor: const Color.fromRGBO(247, 199, 168, 1),
    foregroundColor: const Color.fromARGB(255, 233, 97, 7),
    padding: const EdgeInsets.symmetric(vertical: 10),
    fixedSize: const Size(300, 50),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(5),
    )
  );
  final TextStyle buttonTextStyle = const TextStyle(color: Colors.white,fontSize: 24);

  void _navigateToGermanChat(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => GermanChatPage())
    );
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      backgroundColor: Colors.deepOrange,
      body: SafeArea( // ensures padding from system components (notches, bars etc.)
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Align(
                alignment: Alignment.centerLeft,
                child: Container(
                  padding: const EdgeInsets.only(left: 40, top: 40),
                  child: 
                        const Text('HALLO, \nICH BIN \nAIKA', 
                          textAlign: TextAlign.left,
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 48,
                            fontWeight: FontWeight.bold
                          ),
                        ) 
                  )
              ),
              const SizedBox(height: 50,), // to adjust space between components
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

