
part of 'chat_bloc.dart';

abstract class ChatState extends Equatable {
  const ChatState();

  @override
  List<Object> get props => [];
}

class ChatInitial extends ChatState {}

class ChatLoading extends ChatState {
  final String chatID;
  final List<Message> messages;

  ChatLoading({required this.chatID, required this.messages});

  @override
  List<Object> get props => [chatID, messages];
}

class ChatLoaded extends ChatState {
  final List<Message> messages;
  final String chatID;
  final bool offerLesson;

  ChatLoaded(this.messages, {required this.chatID, this.offerLesson = false});

  @override
  List<Object> get props => [messages, chatID, offerLesson];
}

class LessonLoaded extends ChatState {
  final List<Message> messages;
  final Message lesson;
  final String chatID;

  LessonLoaded(this.messages, this.lesson, {required this.chatID});

  @override
  List<Object> get props => [messages, lesson, chatID];
}

class ChatError extends ChatState {
  final String message;
  final ChatEvent? lastEvent;
  final List<Message> messages;

  ChatError(this.message, this.lastEvent, this.messages);

  @override
  List<Object> get props => [message, lastEvent!, messages];
}