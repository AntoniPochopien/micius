import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/config/env/env.dart';
import 'package:micius_lab_client/data/dto/auth/token_response_dto.dart';
import 'package:micius_lab_client/domain/repository/local_storage_repository.dart';
import 'package:micius_lab_client/domain/services/session_invalidation_notifier.dart';
import 'package:logger/logger.dart';

@lazySingleton
class TokenRefreshService {
  TokenRefreshService(
    @Named('plainDio') this._plainDio,
    this._localStorageRepository,
    this._sessionInvalidationNotifier,
    this._logger,
  );

  final Dio _plainDio;
  final LocalStorageRepository _localStorageRepository;
  final SessionInvalidationNotifier _sessionInvalidationNotifier;
  final Logger _logger;

  Future<String?> refresh() async {
    final refreshToken = await _localStorageRepository.getRefreshToken();
    if (refreshToken == null || refreshToken.isEmpty) {
      _logger.d('Token refresh failed: missing refresh token');
      await _invalidateSession();
      return null;
    }

    _logger.d('Refreshing access token');

    try {
      final response = await _plainDio.post<Map<String, dynamic>>(
        '${Env.apiBaseUrl}/token/refresh',
        data: {'refresh_token': refreshToken},
      );

      final data = response.data;
      if (data == null) {
        _logger.d('Token refresh failed: empty response');
        return null;
      }

      final token = TokenResponseDto.fromJson(data);
      if (token.accessToken.isEmpty) {
        _logger.d('Token refresh failed: empty access token');
        return null;
      }

      await _localStorageRepository.setAccessToken(token.accessToken);
      if (token.refreshToken.isNotEmpty) {
        await _localStorageRepository.setRefreshToken(token.refreshToken);
      }

      _logger.d('Token refresh succeeded');
      return token.accessToken;
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        _logger.d('Token refresh failed: credentials rejected');
        await _invalidateSession();
      } else {
        _logger.d('Token refresh failed: transient error');
      }
      return null;
    }
  }

  Future<void> _invalidateSession() async {
    await _localStorageRepository.clear();
    _sessionInvalidationNotifier.notifySessionInvalidated();
  }
}
