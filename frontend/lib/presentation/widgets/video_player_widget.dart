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
    print('Decoding success');
    // Get the temporary directory
    final tempDir = await getTemporaryDirectory();
    final tempVideoFile = File('${tempDir.path}/temp_video.mp4');

    // Write the bytes to a temporary file
    await tempVideoFile.writeAsBytes(videoBytes);

    // Initialize the video player controller with the temporary file
    print("initializing video controller...");
    VideoPlayerController controller = VideoPlayerController.file(tempVideoFile);
    print("initialized video controller!"); 
    await controller.initialize();
    controller.setVolume(1.0);
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

class VideoControlButtons extends StatefulWidget {
  final VideoPlayerController controller;

  VideoControlButtons({required this.controller});

  @override
  _VideoControlButtonsState createState() => _VideoControlButtonsState();
}

class _VideoControlButtonsState extends State<VideoControlButtons> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller;
    _controller.addListener(_updateState);
  }

  void _updateState() {
    setState(() {});
  }

  @override
  void dispose() {
    _controller.removeListener(_updateState);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
          icon: Icon(_controller.value.isPlaying ? Icons.pause : Icons.play_arrow),
          onPressed: () {
            setState(() {
              _controller.value.isPlaying ? _controller.pause() : _controller.play();
            });
          },
        ),
        IconButton(
          icon: const Icon(Icons.refresh),
          onPressed: () {
            setState(() {
              _controller.pause();
              _controller.seekTo(Duration.zero);
            });
          },
        ),
      ],
    );
  }
}