import 'package:frontend/task_widget/models/task.dart';

Task multipleChoiceTask = Task(
  TaskType.multipleChoice, 
  'What is the correct form of the Perfekt for "Ich gehe"?',
  [
    ['Ich bin gegangen', 'Ich gehe gegangen', 'Ich habe gegangen'],
  ],
  ['Ich bin gegangen'], 
  );

Task fillInTheGapTask = Task(
  TaskType.fillTheGaps,
  'Ich habe gestern einen Film __ und dann __ ich nach Hause gegangen.',
  [
    ['gesehen', 'gekommen', 'gefahren'],
    ['bin', 'habe', 'war']
  ],
  ['gesehen', 'bin'],
);

Task openEndedTask = Task(
  TaskType.openQuestion,
  'Describe in German how you spent your last weekend using Perfekt tense.',
  [['']],
  ['']
);

String dummyLesson = "Let's learn about the Perfekt tense in German. Here is the rule: [Grammar Rule].";