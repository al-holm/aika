import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/styles/app_styles.dart';
import 'package:frontend/utils/l10n/app_localization.dart';

class QuestionListScreen extends StatelessWidget {
  final List<String> questions = [
      'Aus welchen Schritten besteht das Asylverfahren? (Asylantrag, Dublin-Prüfung, Anhörung, Entscheidung)', 'Was ist eine Zulässigkeitsprüfung im Asylverfahren?', 'Was ist das Dublin-Verfahren?', 'Was ist eine Anhörung im Asylverfahren?',
      'Was soll ich vor der Anhörung wissen?', 'Welche Fragen können mir bei der Anhörung gestellt werden?', 'Welche Rechte habe ich bei der Anhörung?', 'Was ist der BAMF-Bescheid?', 'Was ist eine Duldung?', 'Was ist eine Ausbildungsduldung?',
      'Was ist der Chancenaufenthalt § 104c und wann kann ich den bekommen?', 'Was ist § 25a AufenthG und wer kann den beantragen?', 
      'Was ist § 25b AufenthG und wer kann den beantragen?',
    ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppStyles.sandColor,
      appBar: SimpleAppBar(
                text: AppLocalizations.of(context).translate('q_list')),
      body: Container(
        child: _buildQuestionList(context),
      ),
    );
  }


  Widget _buildQuestion(BuildContext context, String question) {
    Size screenSize = MediaQuery.of(context).size;
    return GestureDetector(
        onTap: () {
          final chatBloc = BlocProvider.of<ChatBloc>(context);
          chatBloc.add(SendMessageEvent('law', question));
          Navigator.pop(context);
        }, 
        child : Container(
                padding: EdgeInsets.symmetric(horizontal: screenSize.width*0.025, vertical: screenSize.height*0.01),
                margin:  EdgeInsets.symmetric(horizontal: screenSize.width*0.05, vertical: screenSize.height*0.015),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(4),
                  border: Border.all(color: AppStyles.darkColor, width: 2)
                ),
                child:
                    Text(
                      question,
                      style: AppStyles.questionListstextStyle,
                    ),
              )
      );
  }

  Widget _buildQuestionList(BuildContext context) {
    return ListView.builder(
        shrinkWrap: true,
        itemCount: questions.length,
        itemBuilder: (context, index) {
          final question = '${(index + 1).toString()}. ${questions[index]}';
          return _buildQuestion(context, question);
        }
    );
  }
}