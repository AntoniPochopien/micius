import 'dart:async';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/domain/entity/failure.dart';
import 'package:micius_lab_client/domain/entity/user.dart';
import 'package:micius_lab_client/domain/repository/api_repository.dart';
import 'package:micius_lab_client/domain/repository/local_storage_repository.dart';
import 'package:micius_lab_client/domain/services/session_invalidation_notifier.dart';

part 'auth_state.dart';
part 'auth_cubit.freezed.dart';

@lazySingleton
class AuthCubit extends Cubit<AuthState> {
  AuthCubit(
    this._apiRepository,
    this._localStorageRepository,
    this._sessionInvalidationNotifier,
  ) : super(const AuthState.loading()) {
    _sessionInvalidationSubscription = _sessionInvalidationNotifier.stream
        .listen((_) => unawaited(_onSessionInvalidated()));
  }

  final ApiRepository _apiRepository;
  final LocalStorageRepository _localStorageRepository;
  final SessionInvalidationNotifier _sessionInvalidationNotifier;
  StreamSubscription<void>? _sessionInvalidationSubscription;

  Future<void> _onSessionInvalidated() async {
    await _localStorageRepository.clear();
    if (!isClosed) emit(const AuthState.unauthenticated());
  }

  Future<void> login({
    required String username,
    required String password,
  }) async {
    emit(const AuthState.loading());
    final result = await _apiRepository.login(
      username: username,
      password: password,
    );
    await result.fold(
      (failure) async => emit(AuthState.error(failure)),
      (token) async {
        await (
          _localStorageRepository.setAccessToken(token.accessToken),
          _localStorageRepository.setRefreshToken(token.refreshToken),
        ).wait;
        await fetchUser();
      },
    );
  }

  Future<void> register({
    required String username,
    required String password,
  }) async {
    emit(const AuthState.loading());
    final result = await _apiRepository.register(
      username: username,
      password: password,
    );
    await result.fold(
      (failure) async => emit(AuthState.error(failure)),
      (token) async {
        await (
          _localStorageRepository.setAccessToken(token.accessToken),
          _localStorageRepository.setRefreshToken(token.refreshToken),
        ).wait;
        await fetchUser();
      },
    );
  }

  Future<void> fetchUser() async {
    final accessToken = await _localStorageRepository.getAccessToken();
    final refreshToken = await _localStorageRepository.getRefreshToken();
    if (accessToken == null ||
        accessToken.isEmpty ||
        refreshToken == null ||
        refreshToken.isEmpty) {
      emit(const AuthState.unauthenticated());
      return;
    }

    emit(const AuthState.loading());
    final result = await _apiRepository.getMe();
    result.fold(
      (failure) => emit(AuthState.error(failure)),
      (user) => emit(
        AuthState.authenticated(
          user: user,
          accessToken: accessToken,
          refreshToken: refreshToken,
        ),
      ),
    );
  }

  Future<void> logout() async {
    await _localStorageRepository.clear();
    emit(const AuthState.unauthenticated());
  }

  @override
  Future<void> close() {
    _sessionInvalidationSubscription?.cancel();
    return super.close();
  }
}
