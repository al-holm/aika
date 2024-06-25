import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend/domain/entities/message.dart';
import 'package:frontend/domain/entities/task.dart';
import 'package:frontend/domain/usecases/fetch_lesson.dart';
import 'package:frontend/domain/usecases/fetch_tasks.dart';
import 'package:frontend/domain/usecases/send_image.dart';
import 'package:frontend/domain/usecases/send_message.dart';
import 'package:frontend/utils/metadata_utils.dart';

part 'chat_event.dart';
part 'chat_state.dart';


class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final SendMessage sendMessage;
  final SendImage sendImage;
  final FetchLesson fetchLesson;
  final FetchTasks fetchTasks;
  late String userID;
  final Map<String, List<Message>> chatMessages = {
    'german': [],
    'law': [],
  };

  ChatBloc(this.sendMessage, this.sendImage, this.fetchLesson, this.fetchTasks) : super(ChatInitial()) {
    on<InitializeChatEvent>(_onInitializeChat);
    on<SendMessageEvent>(_onSendMessage);
    on<SendImageEvent>(_onSendImage);
    on<FetchLessonEvent>(_onFetchLesson);
    on<ProposeLessonEvent>(_onProposeLesson);
    on<ClearChatEvent>(_onClearChat);
    on<FetchTaskEvent>(_onFetchTasks);
  }

  void _onInitializeChat(InitializeChatEvent event, Emitter<ChatState> emit) async {
    emit(ChatLoading(chatID: event.chatID, messages: chatMessages[event.chatID]!));
    try {
      if (chatMessages[event.chatID]!.isEmpty) {
      final messages = await _initializeMessages(event.chatID);
      chatMessages[event.chatID] = messages;
      }
      final updatedMessages = List<Message>.from(chatMessages[event.chatID]!);
      emit(ChatLoaded(updatedMessages, chatID: event.chatID, offerLesson: true));
    } catch (e) {
      emit(ChatError("Could not initialize chat", event, state, chatMessages[event.chatID]!));
    }
  }

  void _onSendMessage(SendMessageEvent event, Emitter<ChatState> emit) async {
    ChatState currentState = state;
    if (currentState is ChatLoaded || currentState is LessonLoaded || currentState is ChatError) {
      emit(ChatLoading(chatID: event.chatID, messages: chatMessages[event.chatID]!));
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
        chatMessages[event.chatID]!.add(message);
        final responseMessage = await sendMessage(event.chatID, message);
        chatMessages[event.chatID]!.add(responseMessage);
        final updatedMessages = List<Message>.from(chatMessages[event.chatID]!);
        if (currentState is ChatError) {
           if (currentState.lastState is ChatLoaded) {
            currentState = currentState.lastState as ChatLoaded;
          } else if (currentState.lastState is LessonLoaded) {
            currentState = currentState.lastState as LessonLoaded;
          }
        }
        if (currentState is ChatLoaded) {
          emit(ChatLoaded(updatedMessages, chatID: event.chatID, offerLesson: false));
        } else if (currentState is LessonLoaded) {
          emit(LessonLoaded(updatedMessages, currentState.lesson, chatID: event.chatID));
        } 
      } catch (e) {
        emit(ChatError("Could not send message", event, state, chatMessages[event.chatID]!));
      }
    }
  }

  void _onSendImage(SendImageEvent event, Emitter<ChatState> emit) async {
    final currentState = state;
    if (currentState is ChatLoaded || currentState is LessonLoaded) {
      try {
        await sendImage(event.chatID, event.path);
        add(FetchLessonEvent(event.chatID)); // Fetch responses after sending
      } catch (e) {
        emit(ChatError("Could not send image", event, state, chatMessages[event.chatID]!));
      }
    }
  }

  void _onFetchLesson(FetchLessonEvent event, Emitter<ChatState> emit) async {
    final currentState = state;
    if (currentState is ChatLoaded || currentState is LessonLoaded || currentState is ChatError) {
      emit(ChatLoading(chatID: event.chatID, messages: chatMessages[event.chatID]!));
      try {
        final lesson = await fetchLesson(event.chatID);
        chatMessages[event.chatID]!.add(lesson);
        final updatedMessages = List<Message>.from(chatMessages[event.chatID]!);
        emit(LessonLoaded(updatedMessages, lesson, chatID: event.chatID));
      } catch (e) {
        emit(ChatError("Could not fetch lesson", event, state, chatMessages[event.chatID]!));
      }
    }
  }

    void _onFetchTasks(FetchTaskEvent event, Emitter<ChatState> emit) async {
    final currentState = state;
    if (currentState is ChatLoaded || currentState is LessonLoaded || currentState is ChatError) {
      emit(ChatLoading(chatID: event.chatID, messages: chatMessages[event.chatID]!));
      try {
        final tasks = await fetchTasks(event.chatID);
        emit(TaskLoaded(chatMessages[event.chatID]!, tasks, chatID: event.chatID));
      } catch (e) {
        emit(ChatError("Could not fetch lesson", event, state, chatMessages[event.chatID]!));
      }
    }
  }

  void _onProposeLesson(ProposeLessonEvent event, Emitter<ChatState> emit) {
    final currentState = state;
    if (currentState is TaskLoaded || currentState is LessonLoaded) {
      if (event.previousLessonCompleted) {
        final updatedMessages = List<Message>.from(chatMessages[event.chatID]!);
        emit(ChatLoaded(updatedMessages, chatID: event.chatID, offerLesson: false));
      }
    } else if (currentState is ChatLoaded)  {
      Message message = getLessonOfferingMessage();
      chatMessages[event.chatID]!.add(message);
      final updatedMessages = List<Message>.from(chatMessages[event.chatID]!);
      emit(ChatLoaded(updatedMessages, chatID: event.chatID, offerLesson: true));
    }
  }

  void _onClearChat(ClearChatEvent event, Emitter<ChatState> emit) {
    chatMessages[event.chatID] = [];
    emit(ChatInitial());
  }


  Message getLessonOfferingMessage() {
    final message = Message(
      text: "Gut gemacht! Willst du mit dem neuen Unterricht starten?",
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
    return "Hallo, ich bin AIKA! Ich kann dir helfen, Deutsch zu lernen.\n\nWillst du mit dem neuen Unterricht starten oder hast du Fragen?";
  }

  String getInitMessageLaw() {
    return "Hallo, ich bin AIKA! Ich kann dir helfen, über das Leben in Deutschland mehr zu wissen, Formulare auszufüllen und rechtliche Fragen zu beantworten.\n\nMeine Tipps sind aber nur orientierend, bei Fragen wende dich an eine qualifizierte Beratung. Eine qualifizierte Rechtsberatung bekommst du zum Beispiel hier: www.proasyl.de";
  }
}