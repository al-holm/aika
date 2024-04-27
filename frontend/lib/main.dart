import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart' as intl;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart' as shared_preferences;
import 'package:uuid/uuid.dart' as uuid;

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



class GermanChatPage extends StatefulWidget {
  @override
  _GermanChatState createState() => _GermanChatState();

}


class _GermanChatState extends State {
  final TextEditingController _controller = TextEditingController();
  List<String> _messages = [];
  late String _userId;

  @override
  void initState() {
    super.initState();
    _initUserId();
  }

  Future<void> _initUserId() async {
    final prefs = await shared_preferences.SharedPreferences.getInstance();
    final userId = prefs.getString('userId');
    if (userId != null) {
      setState(() {
        _userId = userId;
      });
    } else {
      final newUserId = const uuid.Uuid().v4(); // Generate new UUID
      await prefs.setString('userId', newUserId); // Save userID in SharedPreferences
      setState(() {
        _userId = newUserId;
      });
    }
  }

  Future<void> _handleSubmitted(String text) async {
    _controller.clear();
    
    // Get current timestamp
    String timestamp = intl.DateFormat('yyyy-MM-dd HH:mm:ss').format(DateTime.now());

    // You need to replace these with actual userId and role values
    String role = 'user';

    // Construct message body with userId, role, and timestamp
    Map<String, dynamic> messageBody = {
      'message': text,
      'userId': _userId,
      'role': role,
      'timestamp': timestamp,
    };

    setState(() {
      _messages.add(text);
      _messages.add("Echo: $text");
    });
/*
    // Send message to backend
    final response = await http.post(
      Uri.parse('https://your-backend-api.com/messages'), // Replace with your backend API URL
      body: messageBody,
    );
    if (response.statusCode == 200) {
      // Decode response JSON
      final responseData = jsonDecode(response.body);
      // Check if response contains a message
      if (responseData.containsKey('message')) {
        setState(() {
          _messages.add(responseData['message']);
        });
      }
    } else {
      // Handle error
    }
*/
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBarAIKA(context),
      body: Column(
        children: <Widget>[
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8),
              reverse: true,
              itemBuilder: (_, int index) => _buildMessageTile(_messages.reversed.toList()[index], context),
                itemCount: _messages.length,
              ),
          ),
          const Divider(height: 1),
          _buildTextInput(_controller, _handleSubmitted)
        ],
      ),
    );
  }
}

Widget _buildMessageTile(String message, BuildContext context) {
  bool isBot = message.startsWith('Echo');
  const double radius = 6;
  var borderRadius = isBot 
          ? const BorderRadius.only(
            topLeft: Radius.circular(radius), 
            topRight: Radius.circular(radius),
            bottomLeft: Radius.circular(0),
            bottomRight: Radius.circular(radius)
          )
          : const BorderRadius.only(
            topLeft: Radius.circular(radius), 
            topRight: Radius.circular(radius),
            bottomLeft: Radius.circular(radius),
            bottomRight: Radius.circular(0)
          );
          
  return Row(
    mainAxisAlignment: isBot? MainAxisAlignment.start : MainAxisAlignment.end,
    children: [
      if (isBot)
        const CircleAvatar(
          child:  Text('B'),
          backgroundColor: Colors.orange,
          foregroundColor: Colors.grey,
          ),
      Container(
        margin: const EdgeInsets.symmetric( horizontal: 8, vertical: 10),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.7),
        decoration: BoxDecoration(
          color: isBot ? Colors.orange : Colors.grey,
          borderRadius: borderRadius,
        ),
        child: Text(message),
      ),
      if (!isBot)
        const CircleAvatar(
          child:  Text('U'),
          backgroundColor: Colors.grey,
          foregroundColor: Colors.orange,
          ),
    ],
    );
}
  

Widget _buildTextInput(_controller, _handleSubmitted) {
  return Padding(
            padding: const EdgeInsets.all(8),
            child: Container(
              decoration: BoxDecoration( 
                border: Border.all(color: Colors.black),
                borderRadius: BorderRadius.circular(5),
              ),
              child: Row(
                children: <Widget>[
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.only(left:10),
                      constraints: BoxConstraints(maxHeight: 200),
                       child: TextField(
                        controller: _controller,
                        onSubmitted: _handleSubmitted,
                        decoration: const InputDecoration.collapsed(hintText: '  Tippen Sie hier...'),
                      ),
                    )
                  ),
                  IconButton(
                    onPressed:() => _controller.text.isNotEmpty ?
                    _handleSubmitted(_controller.text) : null, 
                    icon: const Icon(Icons.send))
                ],
      )
    )
  );
}

AppBar appBarAIKA(BuildContext context) { 
  return AppBar(
    backgroundColor: const Color.fromRGBO(49, 8, 1, 1),
    title: const Text("AIKA", style:TextStyle(color: Colors.white)),
    leading: IconButton(
      icon: const Icon(Icons.arrow_back, color: Colors.white,),
      onPressed: () {
        Navigator.of(context).pop(); // this takes you back to the previous page
      },
    )
    );
}

// read more about TextEditingController, Expanded, Divider, ListView, ListTile
// ToDO - adjustable message box width, display icons under messages