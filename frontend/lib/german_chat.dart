import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart' as intl;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart' as shared_preferences;
import 'package:uuid/uuid.dart' as uuid;
import 'message.dart';
import 'ui_elements.dart';

class GermanChatPage extends StatefulWidget {
  @override
  _GermanChatState createState() => _GermanChatState();

}

/// The `_GermanChatState` class in Dart implements a chat interface with message handling, user ID
/// management, message building, and UI components for sending and displaying messages.
class _GermanChatState extends State {
  late String _userId;
  final TextEditingController _controller = TextEditingController();
  List<Message> _messages = [];


  @override
  void initState() {
    super.initState();
    _initUserId();
    _initMessages();
  }

  /// The `_initMessages` function initializes a chat message with a predefined string and adds it to a
  /// list of messages.
  Future<void> _initMessages() async {
    String initString = "Hallo, ich bin AIKA! Ich kann dir helfen, Deutsch zu lernen, Formulare auszufüllen und rechtliche Fragen zu beantworten.\n\nMeine Tipps sind aber nur orientierend, bei Fragen wende dich an eine qualifizierte Beratung.";
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

  /// The function generates a unique message ID using the Uuid package in Dart.
  /// 
  /// Returns
  /// -------
  /// 	A randomly generated UUID (Universally Unique Identifier) version 4 string is being returned.
  String generateMessageID() {
    return uuid.Uuid().v4();
  }

  /// The _buildMessage function creates a Message object with the provided text, role, and optional
  /// userID.
  /// 
  /// Parameters
  /// ----------
  /// text : String
  /// 	The `text` parameter is the content of the message that will be sent.
  /// role : String
  /// 	The `role` parameter in the `_buildMessage` function is used to specify the role of the user
  /// sending the message. It could be something like "bot", "user".
  /// userID_ : String, optional
  /// 	The `userID_` parameter in the `_buildMessage` function is an optional parameter with a default
  /// value of an empty string `''`. If no value is provided for `userID_`, it will default to an empty
  /// string.
  /// 
  /// Returns
  /// -------
  /// 	A Message object is being returned with the provided text, role, and either the specified userID
  /// or the default userID value. The message also includes a generated messageID and a current
  /// timestamp.
  Message _buildMessage(String text, String role, [String userID_ = '']) {
    String timestamp = getCurrenTimestamp();
    String messageID = generateMessageID();
    String userID = 'null';
    if (userID_ == '') {
      userID = _userId;
    }
    return Message(text: text, userID: userID, 
                  messageID: messageID, role: role, 
                  timestamp: timestamp);

  }
  
  String getCurrenTimestamp() {
    return intl.DateFormat('yyyy-MM-dd HH:mm:ss').format(DateTime.now());
  }

  Map<String, dynamic> getMessageBodyHTTP(Message message) {
  // Construct message body with userId, role, and timestamp
    return  {
      'message': message.getText(),
      'userId': message.getUserID(),
      'messageId': message.getMessageID(),
      'role': message.getRole(),
      'timestamp':message.getTimestamp(),
    };
  }

  Future<void> _handleSubmitted(String text) async {
    if (text == '') return;
    _controller.clear();
    
    Message userMessage = _buildMessage(text, 'user');
    Message botMessage = _buildMessage("Echo: $text", 'bot');

    botMessage.displayMessage();
    setState(() {
      _messages.add(userMessage);
      _messages.add(botMessage);
    });
/*
    // Send message to backend
    messageBody = getMessageBodyHTTP(userMessage);
    final response = await http.post(
      Uri.parse('https://your-backend-api.com/messages'), // Replace with your backend API URL
      body: messageBody,
    );
    if (response.statusCode == 200) {
      // Decode response JSON
      final responseData = jsonDecode(response.body);
      // Check if response contains a message
      if (responseData.containsKey('message')) {
        Message botMessage = Message(text: responseData['message'], userID: _userId, 
                          messageID: generateMessageID(), 
                          role: 'bot', 
                          timestamp: getCurrenTimestamp());
        setState(() {
          _messages.add(botMessage);
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
      backgroundColor: Color.fromRGBO(238, 229, 222, 1),
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
                style: TextStyle(fontFamily: 'SFMono')
        ),
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
                color: Colors.white,
                borderRadius: BorderRadius.circular(5),
              ),
              child: Row(
                children: <Widget>[
                  Expanded(
                    child: Padding(
                        padding: EdgeInsets.only(left:10),
                        child:TextField(
                          controller: _controller,
                          keyboardType: TextInputType.multiline,
                          maxLines: 7,
                          minLines: 1,
                          onSubmitted: _handleSubmitted,
                          decoration: const InputDecoration.collapsed(hintText: '  Tippen Sie hier...'),
                        ),
                      ),
                    ),
                  IconButton(
                    onPressed:() => _handleSubmitted(_controller.text), 
                    icon: const Icon(Icons.send))
                ],
      )
    )
  );
}

