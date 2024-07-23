import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend/domain/entities/credentials.dart';
import 'package:frontend/domain/usecases/send_credentials.dart';

part 'auth_event.dart';
part 'auth_state.dart';

class AuthentificationBloc extends Bloc<AuthentificationEvent, AuthentificationState> {

  final SendCredentials sendCredentials;

  AuthentificationBloc(this.sendCredentials) : super(AuthentificationRequired()) {
    on<SendCredentialsEvent>(_onCredentialsSent);
  }

  void _onCredentialsSent(
      SendCredentialsEvent event, Emitter<AuthentificationState> emit) async {
    emit(AuthentificationPending());
    try {
      // send request to data provider

      Credentials userCredentials = Credentials(
        username: event.username, 
        password: event.password, 
        isSignUp: event.isSignUp);
      String token = await sendCredentials(userCredentials);

      if (token == 'Invalid credentials') {
        emit(AuthentificationFailed(errorMessage: token));
      } else {
        emit(AuthentificationSucceed(sessionToken: token));
      }
    } catch (e) {
      emit(AuthentificationFailed(
          errorMessage: 'Connection Error: try again later.'));
    }
  }
}
