import 'package:flutter/material.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:micius_lab_client/config/l10n/l10n.dart';

part 'failure.freezed.dart';

@freezed
abstract class Failure with _$Failure {
  const factory Failure.unauthorized([String? message]) = _Unauthorized;
  const factory Failure.forbidden([String? message]) = _Forbidden;
  const factory Failure.serverError([String? message]) = _ServerError;
  const factory Failure.unexpected([String? message]) = _Unexpected;
}

extension FailureExtension on Failure {
  String errorMessage(BuildContext context) => map(
    unauthorized: (_) => T(context).unauthorized,
    forbidden: (_) => T(context).forbidden,
    serverError: (_) => T(context).serverError,
    unexpected: (_) => T(context).unexpected,
  );
}
