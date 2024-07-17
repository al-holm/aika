part of 'auth_bloc.dart';

abstract class AuthentificationEvent extends Equatable {
  const AuthentificationEvent();

  @override
  List<Object> get props => [];
}

class SendCredentialsEvent extends AuthentificationEvent {
  final String username;
  final String password;
  final bool isSignUp;

  SendCredentialsEvent(this.username, this.password, this.isSignUp);

  @override
  List<Object> get props => [username, password, isSignUp];
}
