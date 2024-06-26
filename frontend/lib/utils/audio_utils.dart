import 'package:audioplayers/audioplayers.dart';
import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class AudioUtils {
  final AudioPlayer _audioPlayer = AudioPlayer();
  String? audioFilePath;
  Duration maxDuration = Duration();
  Duration elapsedDuration = Duration();
  Stream<Duration> get positionStream => _audioPlayer.onPositionChanged;
  bool isCompleted = false;

  Future<void> prepareAudioFile(String base64Audio) async {
    try {
      final bytes = base64Decode(base64Audio);
      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/audio.mp3');
      await file.writeAsBytes(bytes);
      audioFilePath = file.path;
      _audioPlayer.setSourceDeviceFile(audioFilePath!);
       _audioPlayer.onDurationChanged.listen((duration) {
        maxDuration = duration;
      });
      _audioPlayer.onPlayerComplete.listen((event) {
        isCompleted = true;
        _audioPlayer.seek(Duration.zero);
      });
    } catch (e) {
      print('Error preparing audio file: $e');
    }
  }

  Future<void> playPauseAudio(bool isPlaying) async {
    if (isPlaying) {
      await _audioPlayer.pause();
    } else {
      if (isCompleted) {
        isCompleted = false;
        await _audioPlayer.seek(Duration.zero);
      }
      await _audioPlayer.resume();
    }
  }

  void dispose() {
    _audioPlayer.dispose();
  }
}