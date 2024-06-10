import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/usecases/fetch_lesson.dart';
import 'package:frontend/domain/usecases/send_image.dart';
import 'package:frontend/domain/usecases/send_message.dart';
import 'package:frontend/utils/metadata_utils.dart';

part 'chat_event.dart';
part 'chat_state.dart';

class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final SendMessage sendMessage;
  final SendImage sendImage;
  final FetchLesson fetchLesson;
  late String userID;

  ChatBloc(this.sendMessage, this.sendImage, this.fetchLesson) : super(ChatInitial()) {
    on<InitializeChatEvent>(_onInitializeChat);
    on<SendMessageEvent>(_onSendMessage);
    on<SendImageEvent>(_onSendImage);
    on<FetchLessonEvent>(_onFetchLesson);
    on<ProposeLessonEvent>(_onProposeLesson);
  }

  void _onInitializeChat(InitializeChatEvent event, Emitter<ChatState> emit) async {
    emit(ChatLoading([]));
    try {
      final messages = await _initializeMessages(event.chatID);
      emit(ChatLoaded(messages, offerLesson: true));
    } catch (e) {
      emit(ChatError("Could not initialize chat", event, []));
    }
  }

  void _onSendMessage(SendMessageEvent event, Emitter<ChatState> emit) async {
    final currentState = state;
    if (currentState is ChatLoaded) {
      emit(ChatLoading(currentState.messages));
      try {
        final messageId = MetadataUtils.generateMessageID();
        const role = 'user';
        final timestamp = DateTime.now();
        final message = Message(text:event.content, userID: userID,messageID:  messageId,role:  role, timestamp:  timestamp);
        currentState.messages.add(message);
        final responseMessage = await sendMessage(event.chatID, message);
        final updatedMessages = List<Message>.from(currentState.messages)..add(responseMessage);
        emit(ChatLoaded(updatedMessages, offerLesson: false));
      } catch (e) {
        emit(ChatError("Could not send message", event, currentState.messages));
      }
    } else if (currentState is LessonLoaded) {
      emit(ChatLoading(currentState.messages));
      try {
        final messageId = MetadataUtils.generateMessageID();
        const role = 'user';
        final timestamp = DateTime.now();
        final message = Message(
          text: event.content,
          userID: userID,
          messageID: messageId,
          role: role,
          timestamp: timestamp,
        );
        currentState.messages.add(message);
        final responseMessage = await sendMessage(event.chatID, message);
        final updatedMessages = List<Message>.from(currentState.messages)..add(responseMessage);
        emit(LessonLoaded(updatedMessages, currentState.lesson));
      } catch (e) {
        emit(ChatError("Could not send message", event, currentState.messages));
      }
    }
  }


  void _onSendImage(SendImageEvent event, Emitter<ChatState> emit) async {
    final currentState = state;
    if (currentState is ChatLoaded) {
      try {
        await sendImage(event.chatID, event.path);
        add(FetchLessonEvent(event.chatID)); // Fetch responses after sending
      } catch (e) {
        emit(ChatError("Could not send image", event, currentState.messages));
      }
    }
  }

  void _onFetchLesson(FetchLessonEvent event, Emitter<ChatState> emit) async {
    final currentState = state;
    if (currentState is ChatLoaded) {
      emit(ChatLoading(currentState.messages));
      try {
        final lesson = await fetchLesson(event.chatID);
        final updatedMessages = List<Message>.from(currentState.messages)..add(lesson);
        emit(LessonLoaded(updatedMessages, lesson));
      } catch (e) {
        emit(ChatError("Could not fetch lesson", event, currentState.messages));
      }
    }
  }

  void _onProposeLesson(ProposeLessonEvent event, Emitter<ChatState> emit) {
    final currentState = state;
    if (currentState is LessonLoaded) {
      if (event.previousLessonCompleted) {
        emit(ChatLoaded(currentState.messages));
      }
    } else if (currentState is ChatLoaded)  {
      Message message = getLessonOfferingMessage();
      final updatedMessages = List<Message>.from(currentState.messages)..add(message);
      emit(ChatLoaded(updatedMessages, offerLesson: true));
    }
  }

  Message getLessonOfferingMessage() {
    final message = Message(
      text: "Gut gemacht! Willst du mit dem neuen Untericht starten?",
      userID: 'system',
      messageID: MetadataUtils.generateMessageID(),
      role: 'bot',
      timestamp: DateTime.now(),
    );
    return message;
  }


  Future<List<Message>> _initializeMessages(String chatId) async {
    userID = await MetadataUtils.initUserId();
    if (chatId == 'german') {
      return [
        Message(
          text: getInitMessageGerman(),
          userID: userID,
          messageID: '0',
          role: 'bot',
          timestamp: DateTime.now(),
        )
      ];
    } else if (chatId == 'law') {
      return [
        Message(
          text: getInitMessageLaw(),
          userID: userID,
          messageID: '0',
          role: 'bot',
          timestamp: DateTime.now(),
        ),
      ];
    } else {
      return [];
    }
  }

  String getInitMessageGerman() {
    return "Hallo, ich bin AIKA! Ich kann dir helfen, Deutsch zu lernen.\n\nWillst du mit dem neuen Untericht starten oder hast du Fragen?";
  }

  String getInitMessageLaw() {
    return "Hallo, ich bin AIKA! Ich kann dir helfen, über das Leben in Deutschland mehr zu wissen, Formulare auszufüllen und rechtliche Fragen zu beantworten.\n\nMeine Tipps sind aber nur orientierend, bei Fragen wende dich an eine qualifizierte Beratung.";
  }
}