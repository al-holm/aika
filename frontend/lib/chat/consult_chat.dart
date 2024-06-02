import 'package:frontend/chat/chat.dart';
import 'package:frontend/chat/services/chat_service.dart';
import 'package:frontend/chat/models/message.dart';
import 'package:frontend/chat/widgets/message_tile.dart';

class ConsultChatPage extends ChatPage {
  ConsultChatPage()
      : super(
          apiUrl: 'http://192.168.178.149:3000/german-chat/message/',
          initialMessage: "Hallo, ich bin AIKA! Ich kann dir helfen, über das Leben in Deutschland mehr zu wissen, Formulare auszufüllen und rechtliche Fragen zu beantworten.\n\nMeine Tipps sind aber nur orientierend, bei Fragen wende dich an eine qualifizierte Beratung.",
          appBarTitle: 'Alltag & Recht',
          messageTileBuilder: (message) => MessageTile(message: message),
      );

  @override
  Future<Message?> sendMessage(Message message) async {
    final chatService = ChatService(apiUrl: apiUrl);
    return chatService.sendMessage(message);
  }

  @override
  ConsultChatState createState() => ConsultChatState();
}

class ConsultChatState extends ChatState {}

