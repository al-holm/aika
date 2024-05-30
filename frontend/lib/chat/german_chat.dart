import 'package:frontend/chat/chat.dart';
import 'package:frontend/chat/models/message.dart';
import 'package:frontend/chat/services/chat_service.dart';
import 'package:frontend/chat/widgets/message_tile.dart';

class GermanChatPage extends ChatPage {
  final ChatService chatService = ChatService(apiUrl: 'http://192.168.178.149:3000/german-chat/message/');
  GermanChatPage()
      : super(
          apiUrl: 'http://192.168.178.149:3000/german-chat/message/',
          initialMessage: "Hallo, ich bin AIKA! Ich kann dir helfen, Deutsch zu lernen.\n\nWillst du mit dem neuen Untericht starten oder hast du Fragen?",
          appBarTitle: 'Deutsch',
          messageTileBuilder: (message) => GermanMessageTile(message: message),
        );

  @override
  GermanChatState createState() => GermanChatState();

  @override
  Future<Message?> sendMessage(Message message) {
    return chatService.sendMessage(message);
  }
}

class GermanChatState extends ChatState<GermanChatPage> {
}