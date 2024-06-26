import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:path_provider/path_provider.dart';


class VideoPlayerWidget extends StatelessWidget {
  final String base64Video;

  VideoPlayerWidget({required this.base64Video});

  Future<VideoPlayerController> _initializeVideoPlayer() async {
    // Decode the base64 string into bytes
    Uint8List videoBytes = base64Decode(base64Video);

    // Get the temporary directory
    final tempDir = await getTemporaryDirectory();
    final tempVideoFile = File('${tempDir.path}/temp_video.mp4');

    // Write the bytes to a temporary file
    await tempVideoFile.writeAsBytes(videoBytes);

    // Initialize the video player controller with the temporary file
    VideoPlayerController controller = VideoPlayerController.file(tempVideoFile);
    await controller.initialize();
    return controller;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<VideoPlayerController>(
      future: _initializeVideoPlayer(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        } else if (snapshot.hasData) {
          VideoPlayerController controller = snapshot.data!;
          return Column(
            children: [
              AspectRatio(
                aspectRatio: controller.value.aspectRatio,
                child: VideoPlayer(controller),
              ),
              VideoControlButtons(controller: controller),
            ],
          );
        } else {
          return Center(child: Text('No video available'));
        }
      },
    );
  }
}

class VideoControlButtons extends StatelessWidget {
  final VideoPlayerController controller;

  VideoControlButtons({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
          icon: Icon(controller.value.isPlaying ? Icons.pause : Icons.play_arrow),
          onPressed: () {
            controller.value.isPlaying ? controller.pause() : controller.play();
          },
        ),
        IconButton(
          icon: Icon(Icons.stop),
          onPressed: () {
            controller.pause();
            controller.seekTo(Duration.zero);
          },
        ),
      ],
    );
  }
}