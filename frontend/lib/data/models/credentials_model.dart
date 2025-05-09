

class CredentialsModel {
  final String username;
  final String password;
  final bool isSignUp;

  CredentialsModel({required this.username, 
        required this.password,
        required this.isSignUp});

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'password': password,
      'isSignUp': isSignUp,
    };
  }

}