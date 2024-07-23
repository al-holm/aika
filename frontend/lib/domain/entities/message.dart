enum MessageType{
  message, reading, listening, grammar, listeningVideo
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
      case 'ListeningVideo':
        return MessageType.listeningVideo;
      default:
        return MessageType.message;
    }
  }
}

class Message {
  final String text;
  final String role;
  final MessageType messageType;
  final String audio;
  final String video;

  Message({required this.text, 
        required this.role,
        this.messageType=MessageType.message, this.audio='', this.video=''});
}

