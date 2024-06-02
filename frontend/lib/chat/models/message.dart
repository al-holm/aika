class Message {
  String text;
  String userID;
  String messageID;
  String role;
  DateTime timestamp;
  bool gotTasks = false;

  Message({required this.text, 
        required this.userID,
        required this.messageID, required this.role,
        required this.timestamp});
  
  String getUserID() {
    return userID;
  }

  String getText() {
    return text;
  }

  String getMessageID() {
    return messageID;
  }

  String getRole() {
    return role;
  }

  DateTime getTimestamp() {
    return timestamp;
  }
  
  void displayMessage() {
    print('Message: $text, messageID: $messageID, timestamp: $timestamp, userID: $userID');
  }
}