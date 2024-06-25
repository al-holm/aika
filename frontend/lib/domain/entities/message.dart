enum MessageType{
  message, reading, listening, grammar
}

extension MessageTypeExtension on MessageType {
  static MessageType fromString(String type) {
    switch (type) {
      case 'Reading':
        return MessageType.reading;
      case 'Grammar':
        return MessageType.grammar;
      case 'Listening':
        return MessageType.listening;
      default:
        return MessageType.message;
    }
  }
}

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

