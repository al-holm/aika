part of 'auth_bloc.dart';

class AuthentificationState extends Equatable {
  AuthentificationState();

  @override
  List<Object> get props => [];
}

class AuthentificationPending extends AuthentificationState {
  AuthentificationPending();

  @override
  List<Object> get props => [];
}

class AuthentificationRequired extends AuthentificationState {
  AuthentificationRequired();

  @override
  List<Object> get props => [];
}

class AuthentificationSucceed extends AuthentificationState {
  final String sessionToken;

  AuthentificationSucceed({required this.sessionToken});

  @override
  List<Object> get props => [sessionToken];
}

class AuthentificationFailed extends AuthentificationState {
  final String errorMessage;

  AuthentificationFailed({required this.errorMessage});

  @override
  List<Object> get props => [errorMessage];
}
