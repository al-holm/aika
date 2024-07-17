import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/auth_bloc/auth_bloc.dart';
import 'package:frontend/presentation/widgets/chat_widgets.dart';
import 'package:frontend/presentation/widgets/main_menu_widgets.dart';
import 'package:frontend/presentation/widgets/auth_widgets.dart';
import 'package:frontend/styles/app_styles.dart';

class AuthentificationScreen extends StatelessWidget {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isSignUp = false;

  AuthentificationScreen({super.key});

  void handleSubmitted(BuildContext context) {
    final authBloc = BlocProvider.of<AuthentificationBloc>(context);
    final username = _usernameController.text;
    final password = _passwordController.text;
    if (username.isNotEmpty && password.isNotEmpty) {
      // here send values username, password & isSignUp to server
      authBloc.add(SendCredentialsEvent(username, password, _isSignUp));
      _usernameController.clear();
      _passwordController.clear();
      _isSignUp = false;
    }
    FocusScope.of(context).requestFocus(FocusNode());
  }

  void handleCheckboxState(bool? value) {
    _isSignUp = value ?? false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        resizeToAvoidBottomInset: false,
        backgroundColor: AppStyles.accentColor,
        body: SafeArea(
          child: _buildScreenContent(context),
        ));
  }

  Widget _buildScreenContent(BuildContext context) {
    return BlocListener<AuthentificationBloc, AuthentificationState>(
        listener: (context, state) {
          if (state is AuthentificationSucceed) {
            Navigator.pop(context);
            Navigator.pushNamed(context, '/');
          }
        },
        child: BlocBuilder<AuthentificationBloc, AuthentificationState>(
            builder: (context, state) => _buildScreenState(context, state)));
  }

  Widget _buildScreenState(BuildContext context, AuthentificationState state) {
    if (state is AuthentificationRequired) {
      return buildAuthForm(
          context, false, 'Please sign up or log in to continue');
    } else if (state is AuthentificationFailed) {
      return buildAuthForm(context, true, state.errorMessage);
    } else {
      return buildLoadingScreen(context);
    }
  }

  Center buildLoadingScreen(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double imageDimension = screenSize.width * 0.76;
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const WelcomeTitleWidget(),
          SizedBox(height: screenSize.height * 0.04),
          const LoadingIndicator(),
          SizedBox(height: screenSize.height * 0.04),
          AuthImageContainerWidget(
            imageDimension: imageDimension,
          ),
        ],
      ),
    );
  }

  Center buildAuthForm(BuildContext context, bool isError, String message) {
    Size screenSize = MediaQuery.of(context).size;
    double imageDimension = screenSize.width * 0.76;
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          const WelcomeTitleWidget(),
          SizedBox(height: screenSize.height * 0.04),
          Container(
            padding: EdgeInsets.symmetric(horizontal: screenSize.height * 0.02),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: <Widget>[
                TextFieldAuthWidget(
                  controller: _usernameController,
                  label: 'Username',
                ),
                SizedBox(height: screenSize.height * 0.01),
                TextFieldAuthWidget(
                    controller: _passwordController, label: 'Password'),
                SizedBox(height: screenSize.height * 0.01),
                CheckBoxWidget(
                    isSignUp: _isSignUp, onChanged: handleCheckboxState),
                SizedBox(height: screenSize.height * 0.005),
                Text(
                  message,
                  style: isError
                      ? AppStyles.errorMessageTextStyle
                      : AppStyles.systemMessageTextStyle,
                ),
                SizedBox(height: screenSize.height * 0.01),
                MainMenuButton(
                    text: 'Submit', onPressed: () => handleSubmitted(context)),
                SizedBox(height: screenSize.height * 0.03),
                AuthImageContainerWidget(
                  imageDimension: imageDimension,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
