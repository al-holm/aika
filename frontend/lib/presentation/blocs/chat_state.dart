
part of 'chat_bloc.dart';

abstract class ChatState extends Equatable {
  const ChatState();

  @override
  List<Object> get props => [];
}

class ChatInitial extends ChatState {}

class ChatLoading extends ChatState {
  final List<Message> messages;

  ChatLoading(this.messages);

  @override
  List<Object> get props => [messages];

}

class ChatLoaded extends ChatState {
  final List<Message> messages;
  final bool offerLesson;

  ChatLoaded(this.messages, {this.offerLesson = false});

  @override
  List<Object> get props => [messages, offerLesson];
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
  final ChatEvent? lastEvent;
  final List<Message> messages;

  ChatError(this.message, this.lastEvent, this.messages);

  @override
  List<Object> get props => [message, lastEvent!, messages];
}