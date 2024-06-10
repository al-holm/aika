part of 'chat_bloc.dart';

abstract class ChatEvent extends Equatable {
  const ChatEvent();

  @override
  List<Object> get props => [];
}

class InitializeChatEvent extends ChatEvent {
  final String chatID;

  InitializeChatEvent(this.chatID);

  @override
  List<Object> get props => [chatID];
}

class SendMessageEvent extends ChatEvent {
  final String chatID;
  final String content;

  SendMessageEvent(this.chatID, this.content);

  @override
  List<Object> get props => [chatID, content];
}

class SendImageEvent extends ChatEvent {
  final String chatID;
  final String path;

  SendImageEvent(this.chatID, this.path);

  @override
  List<Object> get props => [chatID, path];
}

class FetchLessonEvent extends ChatEvent {
  final String chatID;

  FetchLessonEvent(this.chatID);

  @override
  List<Object> get props => [chatID];
}

class ProposeLessonEvent extends ChatEvent {
  final bool previousLessonCompleted;
  ProposeLessonEvent(this.previousLessonCompleted);

  @override
  List<Object> get props => [];
}