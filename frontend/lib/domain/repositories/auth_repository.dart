import 'package:frontend/domain/entities/credentials.dart';

abstract class AuthRepository {

  Future<String> sendCredentials(Credentials userCredentials);
  
}