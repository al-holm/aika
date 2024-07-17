import 'dart:math';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

part 'auth_event.dart';
part 'auth_state.dart';

class AuthentificationBloc
    extends Bloc<AuthentificationEvent, AuthentificationState> {
  AuthentificationBloc() : super(AuthentificationRequired()) {
    on<SendCredentialsEvent>(_onCredentialsSent);
  }

  void _onCredentialsSent(
      SendCredentialsEvent event, Emitter<AuthentificationState> emit) {
    emit(AuthentificationPending());
    try {
      // send request to data provider
      print(event.username);
      print(event.password);
      print(event.isSignUp);
      Random random = new Random();
      bool success = random.nextBool(); // dummy logics
      String info = 'Invalid credentials';
      if (success) {
        emit(AuthentificationSucceed(sessionToken: info));
      } else {
        emit(AuthentificationFailed(errorMessage: info));
      }
    } catch (e) {
      emit(AuthentificationFailed(
          errorMessage: 'Connection Error: try again later.'));
    }
  }
}
