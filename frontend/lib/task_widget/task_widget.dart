import 'package:flutter/material.dart';
import 'package:frontend/shared/styles/app_styles.dart';
import 'package:frontend/shared/ui_elements.dart';
import 'package:frontend/utils/app_localization.dart';
import 'package:frontend/task_widget/models/task.dart';

class TaskPage extends StatelessWidget {
  late Task task;

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double padding = screenSize.width * 0.03;

    return Scaffold(
      appBar: appBarAIKA(context, 
        AppLocalizations.of(context).translate('settings')
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Container(
              padding: EdgeInsets.all(padding),
              margin: EdgeInsets.all(padding*1),
              decoration: BoxDecoration(
                color: AppStyles.accentColor,
                borderRadius: BorderRadius.circular(4),
              ),
              ),
          ],
        ),
      ),
    );
  }
}