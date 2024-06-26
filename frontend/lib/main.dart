import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:frontend/data/data_providers/chat_data_provider.dart';
import 'package:frontend/data/data_providers/task_data_provider.dart';
import 'package:frontend/data/repositories/chat_repository_impl.dart';
import 'package:frontend/data/repositories/task_repository_impl.dart';
import 'package:frontend/domain/repositories/chat_repository.dart';
import 'package:frontend/domain/repositories/task_repository.dart';
import 'package:frontend/domain/usecases/fetch_lesson.dart';
import 'package:frontend/domain/usecases/fetch_tasks.dart';
import 'package:frontend/domain/usecases/send_image.dart';
import 'package:frontend/domain/usecases/send_message.dart';
import 'package:frontend/domain/usecases/submit_answers.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/blocs/language_bloc.dart';
import 'package:frontend/presentation/blocs/task_bloc.dart';
import 'package:frontend/presentation/screens/german_chat_screen.dart';
import 'package:frontend/presentation/screens/law_chat_screen.dart';
import 'package:frontend/presentation/screens/main_menu_screen.dart';
import 'package:frontend/presentation/screens/settings_screen.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';
void main() {
  final chatRepository = ChatRepositoryImpl(ChatDataProvider('http://192.168.178.181:3000'));
  final taskRepository = TaskRepositoryImpl(TaskDataProvider('http://192.168.178.181:3000'));
  runApp(MyApp(chatRepository: chatRepository, taskRepository: taskRepository));
}

class MyApp extends StatelessWidget {
  final ChatRepository chatRepository;
  final TaskRepository taskRepository;

  MyApp({required this.chatRepository, required this.taskRepository});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (context) => ChatBloc(
            SendMessage(chatRepository),
            SendImage(chatRepository),
            FetchLesson(chatRepository),
            FetchTasks(chatRepository)
          ),
        ),
        BlocProvider(
          create: (context) => LanguageBloc(),
        ),
        BlocProvider(
          create: (context) => TaskBloc(
            SubmitAnswers(taskRepository),
            BlocProvider.of<ChatBloc>(context),
          ),
        ),
      ],
      child: BlocBuilder<LanguageBloc, LanguageState>(
        builder: (context, state) {
          return MaterialApp(
            debugShowCheckedModeBanner: false,
            title: 'AIKA',
            theme: ThemeData(
              primaryColor: AppStyles.accentColor,
            ),
            locale: state.locale,
            supportedLocales: const [
              Locale('en', ''),
              Locale('de', ''),
              Locale('ru', ''),
              Locale('tr', ''),
            ],
            localizationsDelegates: const [
              AppLocalizations.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            initialRoute: '/',
            routes: {
              '/': (context) => MainMenuScreen(),
              '/german': (context) => GermanChatScreen(),
              '/law': (context) => LawChatScreen(),
              '/settings': (context) => SettingsScreen(),
            },
          );
        },
      ),
    );
  }
}
