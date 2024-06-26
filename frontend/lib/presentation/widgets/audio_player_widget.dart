import 'package:flutter/material.dart';
import 'package:frontend/styles/app_styles.dart';

class AudioPlayer extends StatelessWidget {
  final Duration maxDuration;
  final VoidCallback playPauseAudio;
  final VoidCallback resetAudio;
  final bool isPlaying;
  final Stream<Duration> positionStream;

  const AudioPlayer({
    Key? key,
    required this.maxDuration,
    required this.playPauseAudio,
    required this.resetAudio,
    required this.isPlaying,
    required this.positionStream,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(left: 5, right: 5, bottom: 5),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey, width: 1),
        borderRadius: const BorderRadius.all(Radius.circular(5)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
            onPressed: playPauseAudio,
          ),
          StreamBuilder<Duration>(
            stream: positionStream,
            builder: (context, snapshot) {
              double progress = 0.0;
              if (snapshot.hasData && maxDuration.inMilliseconds > 0) {
                progress = snapshot.data!.inMilliseconds / maxDuration.inMilliseconds;
              }

              return Container(
                height: MediaQuery.of(context).size.height * 0.01,
                width: MediaQuery.of(context).size.width * 0.35,
                child: CustomPaint(
                  painter: ProgressBarPainter(progress),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: resetAudio,
          ),
        ],
      ),
    );
  }
}

class ProgressBarPainter extends CustomPainter {
  final double progress;

  ProgressBarPainter(this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppStyles.accentColor
      ..style = PaintingStyle.fill;

    final progressWidth = size.width * progress;
    canvas.drawRect(Rect.fromLTWH(0, 0, progressWidth, size.height), paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}