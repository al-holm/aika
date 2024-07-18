
import 'package:frontend/domain/entities/credentials.dart';
import 'package:frontend/domain/repositories/auth_repository.dart';

class SendCredentials  {
  final AuthRepository repository;

  SendCredentials(this.repository);

  Future<String> call(Credentials userCredentials) {
    return repository.sendCredentials(userCredentials);
  }
  
}