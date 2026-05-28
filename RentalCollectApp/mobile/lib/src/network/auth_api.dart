import '../models/auth_models.dart';
import 'api_client.dart';

class AuthApi {
  AuthApi(this._api);
  final ApiClient _api;

  Future<String> register({required String name, required String mobile, required String password}) async {
    final json = await _api.postJson('/auth/register', {
      'name': name,
      'mobile': mobile,
      'password': password,
    });
    return (json as Map<String, dynamic>)['id'] as String;
  }

  Future<TokenPair> login({required String mobile, required String password}) async {
    final json = await _api.postForm('/auth/login', {'username': mobile, 'password': password});
    return TokenPair.fromJson(json as Map<String, dynamic>);
  }

  Future<TokenPair> refresh(String refreshToken) async {
    final json = await _api.postJson('/auth/refresh', {'refresh_token': refreshToken});
    return TokenPair.fromJson(json as Map<String, dynamic>);
  }
}

