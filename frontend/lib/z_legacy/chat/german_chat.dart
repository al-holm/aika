import 'package:frontend/z_legacy/chat/chat.dart';
import 'package:frontend/z_legacy/chat/models/message.dart';
import 'package:frontend/z_legacy/chat/services/chat_service.dart';
import 'package:frontend/z_legacy/chat/services/metadata_service.dart';
import 'package:frontend/z_legacy/chat/widgets/message_tile.dart';
import 'package:frontend/z_legacy/task_widget/dummy_tasks.dart';

class GermanChatPage extends ChatPage {
  //'http://192.168.178.184:3000/chat/german/'
  static String url = 'http://192.168.178.184:3000/chat/german/';
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

  Future<List> getLesson() {
    return chatService.getLesson();
  }

}

class GermanChatState extends ChatState<GermanChatPage> {

  @override
  void handleNewLesson() async {
    var lessons = await widget.getLesson();
    setState(() {
      Message lesson_message = Message(
        text: lessons[0],
        userID: 'bot',
        messageID: MetadataService.generateMessageID(),
        role: 'bot',
        timestamp: DateTime.now());
      lesson_message.gotTasks = true;
      lesson_message.tasks = lessons[1];
      messages.add(lesson_message);
    });
  }
}