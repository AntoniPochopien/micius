import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/domain/repository/local_storage_repository.dart';

part 'locale_state.dart';
part 'locale_cubit.freezed.dart';

@lazySingleton
class LocaleCubit extends Cubit<LocaleState> {
  LocaleCubit(this._localStorageRepository) : super(const LocaleState());

  final LocalStorageRepository _localStorageRepository;

  void init() {
    emit(LocaleState(locale: _localStorageRepository.getLocale()));
  }

  Future<void> setLocale(Locale locale) async {
    await _localStorageRepository.setLocale(locale);
    emit(LocaleState(locale: locale));
  }
}
