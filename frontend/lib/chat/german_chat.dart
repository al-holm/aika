import 'package:frontend/chat/chat.dart';
import 'package:frontend/chat/models/message.dart';
import 'package:frontend/chat/services/chat_service.dart';
import 'package:frontend/chat/widgets/message_tile.dart';

class GermanChatPage extends ChatPage {
  static String url = 'http://192.168.178.184:3000/german-chat/message/';
  final ChatService chatService = ChatService(apiUrl: url);
  GermanChatPage()
      : super(
          apiUrl: url,
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