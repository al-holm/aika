import 'package:frontend/z_legacy/task_widget/models/task.dart';

Task multipleChoiceTask = Task(
  TaskType.multipleChoice, 
  'Was sind die Lieblingsfächer des Erzählers?',
  [
    ['Mathematik und Geschichte', 'Mathematik und Biologie', 'Geschichte und Kunst', 'Biologie und Kunst'],
  ],
  ['Mathematik und Geschichte'], 
  );

Task fillInTheGapTask = Task(
  TaskType.fillTheGaps,
  '1. In Mathematik lernen wir gerade __.\n2. Nach der Schule spielen wir oft __ oder gehen ins Kino.]',
  [
    ['Addition', 'Subtraktion', 'Brüche'],
    ['Basketball', 'Tennis', 'Fußball']
  ],
  ['Brüche', 'Fußball'],
);

Task openEndedTask = Task(
  TaskType.openQuestion,
  'Warum mag der Erzähler seine Schule? Nutzen Sie Details aus dem Text.',
  [['']],
  ['']
);

String dummyLesson = "Ich gehe jeden Tag zur Schule. Meine Lieblingsfächer sind Mathematik und Geschichte. In Mathematik lernen wir gerade Brüche und in Geschichte sprechen wir über das Mittelalter. Mein bester Freund heißt Paul und wir sitzen zusammen in der Klasse. Nach der Schule spielen wir oft Fußball oder gehen ins Kino. Unsere Lehrerin, Frau Müller, ist sehr nett und hilft uns immer bei den Hausaufgaben. Ich mag meine Schule sehr.";