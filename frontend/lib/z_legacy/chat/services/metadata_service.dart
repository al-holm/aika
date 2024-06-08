import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

class MetadataService {
  Future<String> initUserId() async {
    final prefs = await SharedPreferences.getInstance();
    final userId = prefs.getString('userId');
    if (userId != null) {
      return userId;
    } else {
      final newUserId = const Uuid().v4();
      await prefs.setString('userId', newUserId);
      return newUserId;
    }
  }

  static String generateMessageID() {
    return const Uuid().v4();
  }

  static DateTime getCurrentTimestamp() {
    return DateTime.now();
  }
}