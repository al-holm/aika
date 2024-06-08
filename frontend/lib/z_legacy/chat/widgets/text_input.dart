import 'package:flutter/material.dart';
import 'package:frontend/z_legacy/shared/styles/app_styles.dart';

class TextInput extends StatelessWidget {
  final TextEditingController controller;
  final Function handleSubmitted;

  const TextInput({required this.controller, required this.handleSubmitted});

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double unitW = screenSize.width * 0.01;
    double unitH = screenSize.height * 0.01;

    void localHandleSubmitted(String text) {
      handleSubmitted(text);
      FocusScope.of(context).requestFocus(FocusNode());
    }

    return Container(
      color: AppStyles.sandColor,
      padding: EdgeInsets.only(left: unitW*2, right: unitW*2, top: unitH*2, bottom: unitH*2),
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: Colors.black),
          color: Colors.white,
          borderRadius: BorderRadius.circular(5),
        ),
        child: Row(
          children: <Widget>[
            Expanded(
              child: Padding(
                padding: EdgeInsets.only(left: unitW*3),
                child: TextField(
                  controller: controller,
                  keyboardType: TextInputType.multiline,
                  maxLines: 7,
                  minLines: 1,
                  onSubmitted: localHandleSubmitted,
                  decoration: const InputDecoration.collapsed(hintText: 'Tippen Sie hier...'),
                ),
              ),
            ),
            IconButton(
              onPressed: () => localHandleSubmitted(controller.text),
              icon: const Icon(Icons.send),
            ),
          ],
        ),
      ),
    );
  }
}