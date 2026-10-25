import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/config/di/interceptors/auth_header_interceptor.dart';
import 'package:micius_lab_client/config/env/env.dart';
import 'package:logger/logger.dart';

@module
abstract class NetworkModule {
  @lazySingleton
  Logger get logger => Logger(
    printer: PrettyPrinter(methodCount: 0, errorMethodCount: 0),
    level: Level.trace,
  );

  @Named('plainDio')
  @lazySingleton
  Dio get plainDio => Dio(
    BaseOptions(
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      sendTimeout: const Duration(seconds: 15),
    ),
  );

  @Named('apiDio')
  @lazySingleton
  Dio apiDio(AuthHeaderInterceptor authHeaderInterceptor) {
    final dio = Dio(
      BaseOptions(
        baseUrl: Env.apiBaseUrl,
        connectTimeout: const Duration(seconds: 15),
        receiveTimeout: const Duration(seconds: 15),
        sendTimeout: const Duration(seconds: 15),
      ),
    );

    dio.interceptors.add(authHeaderInterceptor);
    return dio;
  }
}
