import 'package:frontend/data/data_providers/auth_data_provider.dart';
import 'package:frontend/data/models/credentials_model.dart';
import 'package:frontend/domain/entities/credentials.dart';
import 'package:frontend/domain/repositories/auth_repository.dart';


class AuthRepositoryImpl implements AuthRepository{
  final AuthDataProvider authDataProvider;

  AuthRepositoryImpl(this.authDataProvider);

  @override
  Future<String> sendCredentials(Credentials userCredentials) async {
    CredentialsModel credentialsModel = CredentialsModel(
      username: userCredentials.username, 
      password: userCredentials.password, 
      isSignUp: userCredentials.isSignUp);
    
    final String token = await authDataProvider.sendCredentials(credentialsModel);
    return token;
  }
}