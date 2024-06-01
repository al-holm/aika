import 'package:flutter/material.dart';
class FillInTheGapScreen extends StatefulWidget {
  @override
  _FillInTheGapScreenState createState() => _FillInTheGapScreenState();
}

class _FillInTheGapScreenState extends State<FillInTheGapScreen> {
  final String questionText = 'Flutter is a __ framework for building __ apps from a single codebase.';
  final List<List<String>> answerOptions = [
    ['UI', 'backend', 'database'],
    ['mobile', 'desktop', 'web']
  ];

  final List<String> selectedAnswers = ['', ''];

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Fill in the gaps:',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 16),
          buildQuestion(),
          SizedBox(height: 16),
          ElevatedButton(
            onPressed: checkAnswers,
            child: Text('Submit'),
          ),
        ],
      ),
    );
  }

  Widget buildQuestion() {
    final parts = questionText.split('__');
    final List<Widget> widgets = [];

    for (int i = 0; i < parts.length; i++) {
      widgets.add(Text(parts[i]));
      if (i < answerOptions.length) {
        widgets.add(buildDropdown(i));
      }
    }

    return Wrap(
      children: widgets,
    );
  }

  Widget buildDropdown(int index) {
    return DropdownButton<String>(
      value: selectedAnswers[index].isEmpty ? null : selectedAnswers[index],
      hint: Text('Select'),
      items: answerOptions[index].map((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
      onChanged: (value) {
        setState(() {
          selectedAnswers[index] = value!;
        });
      },
    );
  }

  void checkAnswers() {
    // Implement the logic to check answers
    print('Selected answers: $selectedAnswers');
  }
}