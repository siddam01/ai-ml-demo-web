import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../network/api_client.dart';
import '../network/auth_api.dart';

class SessionStore extends ChangeNotifier {
  static const _kPrefs = 'rentflow.session';

  late SharedPreferences _prefs;
  late ApiClient api;
  late AuthApi auth;

  String baseUrl = 'http://10.0.2.2:8000/api/v1'; // Android emulator default
  String? accessToken;
  String? refreshToken;

  bool get isAuthenticated => accessToken != null && accessToken!.isNotEmpty;

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
    final raw = _prefs.getString(_kPrefs);
    if (raw != null) {
      try {
        final m = jsonDecode(raw) as Map<String, dynamic>;
        baseUrl = (m['baseUrl'] as String?) ?? baseUrl;
        accessToken = m['accessToken'] as String?;
        refreshToken = m['refreshToken'] as String?;
      } catch (_) {
        // ignore invalid cache
      }
    }
    api = ApiClient(baseUrl: baseUrl, getAccessToken: () => accessToken);
    auth = AuthApi(api);
  }

  Future<void> updateBaseUrl(String value) async {
    baseUrl = value.trim();
    api = ApiClient(baseUrl: baseUrl, getAccessToken: () => accessToken);
    auth = AuthApi(api);
    await _persist();
    notifyListeners();
  }

  Future<void> setTokens({required String access, required String refresh}) async {
    accessToken = access;
    refreshToken = refresh;
    await _persist();
    notifyListeners();
  }

  Future<void> logout() async {
    accessToken = null;
    refreshToken = null;
    await _persist();
    notifyListeners();
  }

  Future<void> _persist() async {
    await _prefs.setString(
      _kPrefs,
      jsonEncode({
        'baseUrl': baseUrl,
        'accessToken': accessToken,
        'refreshToken': refreshToken,
      }),
    );
  }
}

