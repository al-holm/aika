import 'package:frontend/chat/chat.dart';
import 'package:frontend/chat/models/message.dart';
import 'package:frontend/chat/services/chat_service.dart';
import 'package:frontend/chat/services/metadata_service.dart';
import 'package:frontend/chat/widgets/message_tile.dart';
import 'package:frontend/task_widget/dummy_tasks.dart';

class GermanChatPage extends ChatPage {
  //'http://192.168.178.184:3000/chat/german/'
  static String url = 'http://192.168.178.34:3000/chat/german/';
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

  Future<bool?> getLesson() {
    return chatService.getLesson();
  }

}

class GermanChatState extends ChatState<GermanChatPage> {

  @override
  void handleNewLesson() async {
    var lessons = await widget.getLesson();
    setState(() {
      Message lesson_message = Message(
        text: dummyLesson,
        userID: 'bot',
        messageID: MetadataService.generateMessageID(),
        role: 'bot',
        timestamp: DateTime.now());
      lesson_message.gotTasks = true;
      messages.add(lesson_message);
    });
  }
}