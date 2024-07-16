import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/presentation/blocs/chat_bloc.dart';
import 'package:frontend/presentation/widgets/app_bar_widgets.dart';
import 'package:frontend/styles/app_styles.dart';

class QuestionListScreen extends StatefulWidget {
  @override
  _QuestionListScreenState createState() => _QuestionListScreenState();
}

class _QuestionListScreenState extends State<QuestionListScreen> {
  final List<String> keys = [
    'Recht',
    'Demokratie & politische Struktur Deutschlands',
    'Deutscher Grundgesetz',
    'Antidiskriminierung',
    'Meinungsfreiheit'
  ];

  final List<List<String>> questions = [
    [
      'Aus welchen Schritten besteht das Asylverfahren? (Asylantrag, Dublin-Prüfung, Anhörung, Entscheidung)',
      'Was ist eine Zulässigkeitsprüfung im Asylverfahren?',
      'Was ist das Dublin-Verfahren?',
      'Was ist eine Anhörung im Asylverfahren?',
      'Was soll ich vor der Anhörung wissen?',
      'Welche Fragen können mir bei der Anhörung gestellt werden?',
      'Welche Rechte habe ich bei der Anhörung?',
      'Was ist der BAMF-Bescheid?',
      'Was ist eine Duldung?',
      'Was ist eine Ausbildungsduldung?',
      'Was ist der Chancenaufenthalt § 104c und wann kann ich den bekommen?',
      'Was ist § 25a AufenthG und wer kann den beantragen?',
      'Was ist § 25b AufenthG und wer kann den beantragen?',
    ],
    [
      'Was bedeutet Demokratie und wie wird sie in Deutschland praktiziert?',
      'Wie funktionieren Wahlen in Deutschland?',
      'Wie ist die politische Struktur Deutschlands aufgebaut?',
      'Wie ist die politische Struktur zwischen Bund und Ländern in Deutschland organisiert und welche Aufgaben haben sie jeweils?',
      'Welche Aufgaben hat der Deutsche Bundestag und wie setzt er sich zusammen?',
      'Wie setzt sich die Bundesregierung zusammen und welche Aufgaben hat sie?',
      'Wie ist die Gewaltenteilung in Deutschland organisiert und warum ist sie wichtig?',
      'Welche Hauptorgane der Europäischen Union gibt es und welche Aufgaben haben sie?',
    ],
    [
      'Welche Bedeutung hat das Grundgesetz für die Bürgerrechte in Deutschland?',
      'Welche Grundrechte sind im Grundgesetz der Bundesrepublik Deutschland verankert?',
      'Was versteht man unter Religionsfreiheit und wie wird sie in Deutschland geschützt?',
    ],
    [
      'Was bedeutet geschlechtergerechte Sprache und warum ist sie wichtig?',
      'Wie wird der Begriff Geschlecht in politischen und sozialen Kontexten verwendet?',
      'Welche Formen von Rassismus gibt es und wie äußern sie sich in der Gesellschaft?',
      'Was ist Antisemitismus und welche Maßnahmen gibt es in Deutschland, um ihn zu bekämpfen?',
      'Was versteht man unter Sexismus und welche Auswirkungen hat er auf die Gleichstellung der Geschlechter?',
      'Welche Herausforderungen und Rechte haben trans Personen in Deutschland?',
    ],
    [
      'Was sind Verschwörungstheorien und warum sind sie für die Gesellschaft problematisch?',
      'Was bedeutet Zensur und welche Auswirkungen hat sie auf die Meinungsfreiheit?',
    ],
  ];

  List<bool> _isOpen = [];

  @override
  void initState() {
    super.initState();
    _isOpen = List<bool>.filled(keys.length, false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppStyles.sandColor,
      appBar: SimpleAppBar(text: 'Fragenkatalog'),
      body: _buildQuestionList(),
    );
  }

  Widget _buildQuestion(BuildContext context, String question, int panelIndex) {
    Size screenSize = MediaQuery.of(context).size;
    return GestureDetector(
      onTap: () {
        final chatBloc = BlocProvider.of<ChatBloc>(context);
        chatBloc.add(SendMessageEvent('law', question));
        setState(() {
          _isOpen[panelIndex] =
              false; // Collapse the panel when a question is clicked
        });
        Navigator.pop(context);
      },
      child: Container(
        padding: EdgeInsets.symmetric(
            horizontal: screenSize.width * 0.025,
            vertical: screenSize.height * 0.01),
        margin: EdgeInsets.symmetric(
            horizontal: screenSize.width * 0.05,
            vertical: screenSize.height * 0.015),
        decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(4),
            border: Border.all(color: AppStyles.darkColor, width: 2)),
        child: Text(
          question,
          style: AppStyles.questionListstextStyle,
        ),
      ),
    );
  }

  Widget _buildQuestionList() {
    return SingleChildScrollView(
      child: ExpansionPanelList(
        expansionCallback: (int index, bool isExpanded) {
          setState(() {
            _isOpen[index] = !isExpanded;
          });
        },
        children: keys.asMap().entries.map<ExpansionPanel>((entry) {
          int index = entry.key;
          String key = entry.value;
          return ExpansionPanel(
            backgroundColor: AppStyles.sandColor,
            headerBuilder: (BuildContext context, bool isExpanded) {
              return ListTile(
                title: GestureDetector(
                  onTap: () {
                    setState(() {
                      _isOpen[index] = !_isOpen[index];
                    });
                  },
                  child: Text(key, style: AppStyles.questionListstextStyle),
                ),
              );
            },
            body: Column(
              children: questions[index]
                  .map((question) => _buildQuestion(context, question, index))
                  .toList(),
            ),
            isExpanded: _isOpen[index],
          );
        }).toList(),
      ),
    );
  }
}
