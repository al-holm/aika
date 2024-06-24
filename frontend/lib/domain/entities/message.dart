class Message {
  final String text;
  final String userID;
  final String messageID;
  final String role;
  final DateTime timestamp;
  final bool hasTasks;

  Message({required this.text, 
        required this.userID,
        required this.messageID, required this.role,
        required this.timestamp,
        this.hasTasks = false});
}

