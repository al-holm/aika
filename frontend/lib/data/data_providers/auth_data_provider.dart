import 'dart:convert';
import 'package:frontend/data/models/credentials_model.dart';
import 'package:http/http.dart' as http;



class AuthDataProvider {

  final String baseUrl;

  AuthDataProvider(this.baseUrl);

  Future<String> sendCredentials(CredentialsModel userCredentials) async {

    print('AUTH: SENDING HTTP REQUEST');
    print(userCredentials.username);
    print(userCredentials.password);
    print(userCredentials.isSignUp);

    final response = await http.post(
      Uri.parse('$baseUrl/auth'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(userCredentials.toJson()),
    );

    if (response.statusCode == 201) {
      final String token = json.decode(response.body)['token'];
      return token;
    } else {
      throw Exception('Failed to fetch a response');
    }

  }
}