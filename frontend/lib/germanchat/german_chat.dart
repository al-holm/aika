import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart' as intl;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart' as shared_preferences;
import 'package:uuid/uuid.dart' as uuid;
import 'message.dart';
import '../shared/ui_elements.dart';


class GermanChatPage extends StatefulWidget {
  @override
  _GermanChatState createState() => _GermanChatState();

}

/// implements a chat interface with message handling, user ID management, 
/// message building, and UI components for sending and displaying messages.
class _GermanChatState extends State {
  late String _userId;
  final TextEditingController _controller = TextEditingController();
  List<Message> _messages = [];
  bool isLoading = false;


  @override
  void initState() {
    super.initState();
    _initUserId();
    _initMessages();
  }

  /// The `_initMessages` function initializes a chat message with a predefined string and adds it to a
  /// list of messages.
  Future<void> _initMessages() async {
    String initString = "Hallo, ich bin AIKA! Ich kann dir helfen, Deutsch zu lernen.\n\nWillst du mit dem neuen Untericht starten oder hast Fragen?";
    Message initMessage = _buildMessage(initString, 'bot', 'init');
    setState(() {
         _messages.add(initMessage);
      }
    );
  }
  

  /// The `_initUserId` function checks if a user ID exists in SharedPreferences, generates a new UUID
  /// if not, and saves it in SharedPreferences.
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

/// generates messsage ids
  String generateMessageID() {
    return uuid.Uuid().v4();
  }

/// builds message object 
  Message _buildMessage(String text, String role, [String userID_ = '']) {
    DateTime timestamp = getCurrenTimestamp();
    String messageID = generateMessageID();
    String userID = 'null';
    if (userID_ == '') {
      userID = _userId;
    }
    return Message(text: text, userID: userID, 
                  messageID: messageID, role: role, 
                  timestamp: timestamp);

  }
  
/// gets current time stamp
  DateTime getCurrenTimestamp() {
    return DateTime.now();
  }

/// constructs body of the request and encodes it to JSON
  String getMessageBodyHTTP(Message message) {
  // Construct message body with userId, role, and timestamp
    return  jsonEncode(<String, dynamic>{
      'message_text': message.getText(),
      'user_id': message.getUserID(),
      'message_id': message.getMessageID(),
      'role': message.getRole(),
      'timestamp':message.getTimestamp().toIso8601String(),
    });
  }
/// sends a POST requests to a backend and updates messages List<Message>
  Future<void> _handleSubmitted(String text) async {
    if (text == '') return;
    _controller.clear();
    
    Message userMessage = _buildMessage(text, 'user');
    //Message botMessage = _buildMessage("Echo: $text", 'bot');

    setState(() {
      _messages.add(userMessage);
      isLoading = true;
    });
    // Send message to backend
    var messageBody = getMessageBodyHTTP(userMessage);
    final url = Uri.parse('http://10.0.2.2:3000/german-chat/message/'); // IP of Android emulator
    final response = await http.post(
      url, // Replace with your backend API URL
      headers: {"Content-Type": "application/json"},
      body: messageBody,
    );
    if (response.statusCode == 201) {
      // Decode response JSON
      final responseData = jsonDecode(response.body)['message'];
      // Check if response contains a message
      if (responseData.containsKey('message_text')) {
        Message botMessage = Message(text: responseData['message_text'], 
                          userID: responseData['user_id'], 
                          messageID: responseData['message_id'], 
                          role: responseData['role'], 
                          timestamp: DateTime.parse(responseData['timestamp']));
        setState(() {
          _messages.add(botMessage);
          isLoading = false;
        });
      }
    } else {
      print(response.statusCode);
    }
  }

/// builds widget
  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Scaffold(
      backgroundColor: Color.fromRGBO(238, 229, 222, 1),
      appBar: appBarAIKA(context, 'AIKA Chat'),
      body: Column(
        children: <Widget>[
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.only(top: 20, left: 8, right: 8, bottom: 20),
              reverse: true,
              itemBuilder: (_, int index) => _buildMessageTile(_messages.reversed.toList()[index], context),
                itemCount: _messages.length,
              ),
          ),
          if (isLoading) // Display loading indicator when loading
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8.0),
                child: _buildLoadingIndicator(),
              ),
          const Divider(height: 1),
          _buildTextInput(_controller, _handleSubmitted, context)
        ],
      ),
    )
    );
  }
}

/// builds message containining avatar, message box wrapping a message text
Widget _buildMessageTile(Message message, BuildContext context) {
  bool isBot = message.role == 'bot';
  const double radius = 15;
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
    mainAxisAlignment: isBot? MainAxisAlignment.start: MainAxisAlignment.end,
    crossAxisAlignment: CrossAxisAlignment.end,
    children: [
      if (isBot)
        Container(
            width: 60.0,  // Diameter of the circle
            height: 60.0, // Diameter of the circle
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage('assets/images/bot_avatar.png'), // Path to your image asset
                fit: BoxFit.scaleDown,
              ),
              shape: BoxShape.circle,
            ),
          ),
      Container(
        margin: const EdgeInsets.symmetric( horizontal: 8, vertical: 10),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.7),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: borderRadius,
          border: Border.all(color: Colors.black, width: 1.5)
        ),
        child: Text(message.text, 
                style: const TextStyle(fontFamily: 'SFMono', fontSize: 17)
        ),
      ),
    ],
    );
}
  

/// builds text input fuild, ensures the margins and handles message submission
Widget _buildTextInput(TextEditingController _controller, Function _handleSubmitted, BuildContext context) {
  Size screenSize = MediaQuery.of(context).size;

  // Define a local method that handles text submission and also hides the keyboard.
  void _localHandleSubmitted(String text) {
    _handleSubmitted(text); // Call the original handle submitted method
    FocusScope.of(context).requestFocus(FocusNode()); // This will hide the keyboard
  }

  return Padding(
    padding: EdgeInsets.only(left: 8, right: 8, top: 10, bottom: screenSize.height * 0.03),
    child: Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black),
        color: Colors.white,
        borderRadius: BorderRadius.circular(5),
      ),
      child: Row(
        children: <Widget>[
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(left: 10),
              child: TextField(
                controller: _controller,
                keyboardType: TextInputType.multiline,
                maxLines: 7,
                minLines: 1,
                onSubmitted: _localHandleSubmitted,  // Update to use local handle submitted
                decoration: const InputDecoration.collapsed(hintText: 'Tippen Sie hier...'),
              ),
            ),
          ),
          IconButton(
            onPressed: () => _localHandleSubmitted(_controller.text),  // Use the local function to hide keyboard
            icon: const Icon(Icons.send),
          ),
        ],
      ),
    ),
  );
}

Widget _buildLoadingIndicator() {
  return Row(
    mainAxisAlignment: MainAxisAlignment.center,
    children: <Widget>[
      Dot(),
      SizedBox(width: 4),
      Dot(),
      SizedBox(width: 4),
      Dot(),
    ],
  );
}

class Dot extends StatefulWidget {
  @override
  _DotState createState() => _DotState();
}

class _DotState extends State<Dot> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 1000),
      vsync: this,
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _controller.drive(
        CurveTween(curve: Curves.easeInOut),
      ),
      child: Container(
        margin: EdgeInsets.all(15),
        width: 8,
        height: 8,
        decoration: BoxDecoration(
          color: Colors.black,
          shape: BoxShape.circle,
        ),
      ),
    );
  }
}
