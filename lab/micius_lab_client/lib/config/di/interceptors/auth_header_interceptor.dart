import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/data/services/token_refresh_service.dart';
import 'package:micius_lab_client/domain/repository/local_storage_repository.dart';
import 'package:logger/logger.dart';

@lazySingleton
class AuthHeaderInterceptor extends QueuedInterceptor {
  static const _retriedExtraKey = 'authRetried';

  AuthHeaderInterceptor(
    this._logger,
    this._localStorageRepository,
    this._tokenRefreshService,
    this._plainDio,
  );

  final Logger _logger;
  final LocalStorageRepository _localStorageRepository;
  final TokenRefreshService _tokenRefreshService;
  final Dio _plainDio;

  static const _publicPaths = {
    '/health',
    '/register',
    '/token',
    '/token/refresh',
  };

  bool _isPublicRequest(RequestOptions options) =>
      _publicPaths.contains(options.path);

  String? _bearerFrom(RequestOptions options) {
    final header = options.headers['Authorization']?.toString();
    if (header == null || !header.startsWith('Bearer ')) return null;
    return header.substring(7);
  }

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    if (!_isPublicRequest(options) && options.headers['Authorization'] == null) {
      final accessToken = await _localStorageRepository.getAccessToken();
      if (accessToken != null && accessToken.isNotEmpty) {
        options.headers['Authorization'] = 'Bearer $accessToken';
      }
    }

    _logger.d(
      'Request: ${options.method} ${options.path}\n'
      'Payload: ${options.data}',
    );
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    _logger.d('Response: ${response.data}');
    handler.next(response);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode != 401 ||
        _isPublicRequest(err.requestOptions) ||
        err.requestOptions.extra[_retriedExtraKey] == true) {
      return handler.next(err);
    }

    final requestToken = _bearerFrom(err.requestOptions);
    final storedToken = await _localStorageRepository.getAccessToken();

    String? accessToken;
    if (storedToken != null &&
        storedToken.isNotEmpty &&
        storedToken != requestToken) {
      accessToken = storedToken;
    } else {
      accessToken = await _tokenRefreshService.refresh();
      if (accessToken == null) {
        return handler.next(err);
      }
    }

    final request = err.requestOptions;
    request.headers['Authorization'] = 'Bearer $accessToken';
    request.extra[_retriedExtraKey] = true;

    try {
      final response = await _plainDio.fetch(request);
      return handler.resolve(response);
    } on DioException catch (retryError) {
      return handler.next(retryError);
    }
  }
}
