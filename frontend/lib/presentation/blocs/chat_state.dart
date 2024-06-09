
part of 'chat_bloc.dart';

abstract class ChatState extends Equatable {
  const ChatState();

  @override
  List<Object> get props => [];
}

class ChatInitial extends ChatState {}

class ChatLoading extends ChatState {}

class ChatLoaded extends ChatState {
  final List<Message> messages;
  bool hasLesson = false;

  ChatLoaded(this.messages, {this.hasLesson = false});

  @override
  List<Object> get props => [messages, hasLesson];
}

class LessonLoaded extends ChatState {
  final List<Message> messages;
  final Message lesson;

  LessonLoaded(this.messages, this.lesson);

  @override
  List<Object> get props => [messages, lesson];
}

class ChatError extends ChatState {
  final String message;

  ChatError(this.message);

  @override
  List<Object> get props => [message];
}