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

  AudioUtils() {
    _audioPlayer.onDurationChanged.listen((duration) {
      maxDuration = duration;
    });
    _audioPlayer.onPositionChanged.listen((duration) {
      elapsedDuration = duration;
      if (maxDuration <= elapsedDuration) {
        _audioPlayer.pause();
      }
    });
  }

  Future<void> prepareAudioFile(String base64Audio) async {
    try {
      final bytes = base64Decode(base64Audio);
      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/audio.mp3');
      await file.writeAsBytes(bytes);
      audioFilePath = file.path;
      await _audioPlayer.setSourceDeviceFile(audioFilePath!);
    } catch (e) {
      print('Error preparing audio file: $e');
    }
  }

  Future<void> playPauseAudio(bool isPlaying) async {
    try {
      if (isPlaying) {
        await _audioPlayer.pause();
      } else {
        await _audioPlayer.resume();
      }
    } catch (e) {
      print('Error in playPauseAudio: $e');
    }
  }

  Future<void> resetAudio() async {
    try {
      await _audioPlayer.pause();
      await _audioPlayer.stop();
      await _audioPlayer.setSourceDeviceFile(audioFilePath!);
      elapsedDuration = Duration.zero;
      print('reset audio');
    } catch (e) {
      print('Error in resetAudio: $e');
    }
  }

  void dispose() {
    _audioPlayer.dispose();
  }
}