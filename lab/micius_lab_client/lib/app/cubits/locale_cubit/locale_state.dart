part of 'locale_cubit.dart';

@freezed
abstract class LocaleState with _$LocaleState {
  const factory LocaleState({Locale? locale}) = _LocaleState;
}