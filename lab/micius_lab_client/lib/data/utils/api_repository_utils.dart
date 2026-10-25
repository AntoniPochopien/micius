import 'package:dio/dio.dart';
import 'package:micius_lab_client/domain/entity/failure.dart';

class ApiRepositoryUtils {
  static Future<Failure> handleFailure(
    Object e, [
    StackTrace? stackTrace,
  ]) async {
    try {
      if (e is! DioException) {
        return Failure.unexpected(e.toString());
      }

      if (e.type == DioExceptionType.badResponse) {
        return _buildFailureFromBadResponse(e);
      }

      return Failure.unexpected(e.message);
    } catch (_) {
      return const Failure.unexpected();
    }
  }

  static Failure _buildFailureFromBadResponse(DioException e) {
    final statusCode = e.response?.statusCode;
    final message = _extractMessage(e);

    return switch (statusCode) {
      401 => Failure.unauthorized(message),
      403 => Failure.forbidden(message),
      final code when code != null && code >= 500 => Failure.serverError(
        message,
      ),
      _ => Failure.unexpected(message),
    };
  }

  static String? _extractMessage(DioException e) {
    final responseData = e.response?.data;
    if (responseData is Map) {
      final detail = responseData['detail'] ?? responseData['message'];
      if (detail is String && detail.isNotEmpty) {
        return detail;
      }
    }
    return e.message;
  }
}
