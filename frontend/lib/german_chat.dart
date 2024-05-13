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
  
  DateTime getCurrenTimestamp() {
    return DateTime.now();
  }

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

  Future<void> _handleSubmitted(String text) async {
    if (text == '') return;
    _controller.clear();
    
    Message userMessage = _buildMessage(text, 'user');
    //Message botMessage = _buildMessage("Echo: $text", 'bot');

    setState(() {
      _messages.add(userMessage);
      //_messages.add(botMessage);
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
      print(responseData);
      // Check if response contains a message
      if (responseData.containsKey('message_text')) {
        Message botMessage = Message(text: responseData['message_text'], 
                          userID: responseData['user_id'], 
                          messageID: responseData['message_id'], 
                          role: responseData['role'], 
                          timestamp: DateTime.parse(responseData['timestamp']));
        setState(() {
          _messages.add(botMessage);
        });
      }
    } else {
      print(response.statusCode);
    }
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
              padding: const EdgeInsets.only(top: 20, left: 8, right: 8, bottom: 20),
              reverse: true,
              itemBuilder: (_, int index) => _buildMessageTile(_messages.reversed.toList()[index], context),
                itemCount: _messages.length,
              ),
          ),
          const Divider(height: 1),
          _buildTextInput(_controller, _handleSubmitted, context)
        ],
      ),
    );
  }
}

/// The _buildMessageTile function creates a message tile
/// @param {Message} message - The `message` parameter in the `_buildMessageTile` function represents an
/// object of type `Message`. It contains information about a message, such as the role (e.g., 'bot' or
/// user) and the text content of the message. The function uses this information to construct a visual
/// representation
/// @param {BuildContext} context - The `context` parameter in the `_buildMessageTile` function is of
/// type `BuildContext`. It represents the location of the widget in the widget tree. The `BuildContext`
/// is used to access information about the location of the widget in the widget tree, such as the
/// theme, media query data,
/// @returns A widget representing a message tile is being returned. The message tile includes an avatar
/// (if the message is from a bot), a container displaying the message text, and styling based on
/// whether the message is from a bot or not.
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
  

/// The _buildTextInput function creates a text input field with a send button that calls a
/// handleSubmitted function and hides the keyboard after submission.
/// @param {TextEditingController} _controller - The `_controller` parameter in the `Widget
/// _buildTextInput` function is of type `TextEditingController`. This controller is used to control the
/// text field widget in the UI. It allows you to read the text that has been entered into the text
/// field and also to set or update the text programmatically
/// @param {Function} _handleSubmitted - The `_handleSubmitted` function is a callback function that is
/// called when the user submits text input. It is used to handle the submitted text in some way, such
/// as processing it or sending it to a server. In the provided code snippet, it is passed as a
/// parameter to the `_buildTextInput
/// @param {BuildContext} context - The `context` parameter in the `_buildTextInput` function represents
/// the build context of the widget. It is typically used to access information about the location of
/// the widget in the widget tree and to interact with other widgets or services in the app.
/// @returns The function `_buildTextInput` is returning a `Padding` widget containing a `Container`
/// widget with a border, color, and borderRadius. Inside the `Container`, there is a `Row` widget with
/// two children: an `Expanded` widget containing a `TextField` and an `IconButton`. The `TextField`
/// allows multiline input and has a hint text. The `IconButton` triggers the `_local
Widget _buildTextInput(TextEditingController _controller, Function _handleSubmitted, BuildContext context) {
  Size screenSize = MediaQuery.of(context).size;

  // Define a local method that handles text submission and also hides the keyboard.
  void _localHandleSubmitted(String text) {
    _handleSubmitted(text); // Call the original handle submitted method
    FocusScope.of(context).requestFocus(new FocusNode()); // This will hide the keyboard
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
              padding: EdgeInsets.only(left: 10),
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

