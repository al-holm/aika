import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';

class GermanChatAppBar extends StatelessWidget implements PreferredSizeWidget {
  @override
  Widget build(BuildContext context) {
    final chatBloc = BlocProvider.of<ChatBloc>(context);
    return AppBar(
      title: const Text('Deutsch',),
      backgroundColor: AppStyles.darkColor,
      foregroundColor: AppStyles.sandColor,
      actions: [
        IconButton(
          icon: const Icon(Icons.school),
          color: AppStyles.sandColor,
          onPressed: () {
            chatBloc.add(FetchLessonEvent('german'));
          },
        ),
        IconButton(
          icon: const Icon(Icons.settings),
          color: AppStyles.sandColor,
          onPressed: () {
            Navigator.pushNamed(context, '/settings');
          },
        ),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}