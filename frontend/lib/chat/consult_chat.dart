import 'package:frontend/chat/chat.dart';
import 'package:frontend/chat/services/chat_service.dart';
import 'package:frontend/chat/models/message.dart';
import 'package:frontend/chat/widgets/message_tile.dart';

class ConsultChatPage extends ChatPage {
  // 'http://192.168.178.184:3000/chat/law/'
  static String url = 'http://10.192.104.214:3000/chat/law/';
  final ChatService chatService = ChatService(apiUrl: url);
  ConsultChatPage()
      : super(
          apiUrl: url,
          initialMessage: "Hallo, ich bin AIKA! Ich kann dir helfen, über das Leben in Deutschland mehr zu wissen, Formulare auszufüllen und rechtliche Fragen zu beantworten.\n\nMeine Tipps sind aber nur orientierend, bei Fragen wende dich an eine qualifizierte Beratung.",
          appBarTitle: 'Alltag & Recht',
          messageTileBuilder: (message) => MessageTile(message: message),
      );

  @override
  Future<Message?> sendMessage(Message message) async {
    return chatService.sendMessage(message);
  }

  @override
  ConsultChatState createState() => ConsultChatState();
}

class ConsultChatState extends ChatState {}

