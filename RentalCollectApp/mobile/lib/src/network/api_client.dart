import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final int statusCode;
  final String message;
  final dynamic body;

  ApiException({required this.statusCode, required this.message, this.body});

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class ApiClient {
  ApiClient({required String baseUrl, required String? Function() getAccessToken})
      : _baseUrl = baseUrl.replaceAll(RegExp(r'/$'), ''),
        _getAccessToken = getAccessToken;

  final String _baseUrl;
  final String? Function() _getAccessToken;

  Uri _uri(String path, [Map<String, String>? query]) {
    final p = path.startsWith('/') ? path : '/$path';
    return Uri.parse('$_baseUrl$p').replace(queryParameters: query);
  }

  Map<String, String> _headers({bool jsonBody = true, Map<String, String>? extra}) {
    final headers = <String, String>{};
    if (jsonBody) headers['Content-Type'] = 'application/json';
    final token = _getAccessToken();
    if (token != null && token.isNotEmpty) {
      headers['Authorization'] = 'Bearer $token';
    }
    if (extra != null) headers.addAll(extra);
    return headers;
  }

  Future<dynamic> getJson(String path, {Map<String, String>? query}) async {
    final res = await http.get(_uri(path, query), headers: _headers(jsonBody: false));
    return _decodeOrThrow(res);
  }

  Future<dynamic> postJson(String path, Object body) async {
    final res = await http.post(_uri(path), headers: _headers(), body: jsonEncode(body));
    return _decodeOrThrow(res);
  }

  Future<dynamic> patchJson(String path, Object body) async {
    final res = await http.patch(_uri(path), headers: _headers(), body: jsonEncode(body));
    return _decodeOrThrow(res);
  }

  Future<void> delete(String path) async {
    final res = await http.delete(_uri(path), headers: _headers(jsonBody: false));
    if (res.statusCode == 204) return;
    _decodeOrThrow(res);
  }

  Future<dynamic> postForm(String path, Map<String, String> form) async {
    final res = await http.post(
      _uri(path),
      headers: _headers(jsonBody: false, extra: {'Content-Type': 'application/x-www-form-urlencoded'}),
      body: form,
    );
    return _decodeOrThrow(res);
  }

  dynamic _decodeOrThrow(http.Response res) {
    if (res.statusCode >= 200 && res.statusCode < 300) {
      if (res.body.isEmpty) return null;
      return jsonDecode(res.body);
    }
    dynamic decoded;
    try {
      decoded = res.body.isEmpty ? null : jsonDecode(res.body);
    } catch (_) {
      decoded = res.body;
    }
    throw ApiException(
      statusCode: res.statusCode,
      message: 'Request failed',
      body: decoded,
    );
  }
}

