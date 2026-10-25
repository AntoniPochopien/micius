import 'package:flutter/material.dart';

abstract final class AppColors {
  static const transparent = Colors.transparent;
  static const white = Color(0xFFFFFFFF);
  static const black = Color(0xFF111827);
  static const primary = Color(0xFF2563EB);
  static const secondary = Color(0xFFDBEAFE);
  static const textSecondary = Color(0xFF6B7280);
  static const surface = Color(0xFFF9FAFB);
  static const border = Color(0xFFD1D5DB);
  static const disabled = Color(0xFFE5E7EB);
  static const error = Color(0xFFDC2626);
}

class AppColorsTheme extends ThemeExtension<AppColorsTheme> {
  const AppColorsTheme._({
    required this.transparent,
    required this.white,
    required this.black,
    required this.primary,
    required this.secondary,
    required this.textSecondary,
    required this.surface,
    required this.border,
    required this.disabled,
    required this.error,
  });

  factory AppColorsTheme.light() => const AppColorsTheme._(
    transparent: AppColors.transparent,
    white: AppColors.white,
    black: AppColors.black,
    primary: AppColors.primary,
    secondary: AppColors.secondary,
    textSecondary: AppColors.textSecondary,
    surface: AppColors.surface,
    border: AppColors.border,
    disabled: AppColors.disabled,
    error: AppColors.error,
  );

  final Color transparent;
  final Color white;
  final Color black;
  final Color primary;
  final Color secondary;
  final Color textSecondary;
  final Color surface;
  final Color border;
  final Color disabled;
  final Color error;

  @override
  AppColorsTheme copyWith({
    Color? transparent,
    Color? white,
    Color? black,
    Color? primary,
    Color? secondary,
    Color? textSecondary,
    Color? surface,
    Color? border,
    Color? disabled,
    Color? error,
  }) {
    return AppColorsTheme._(
      transparent: transparent ?? this.transparent,
      white: white ?? this.white,
      black: black ?? this.black,
      primary: primary ?? this.primary,
      secondary: secondary ?? this.secondary,
      textSecondary: textSecondary ?? this.textSecondary,
      surface: surface ?? this.surface,
      border: border ?? this.border,
      disabled: disabled ?? this.disabled,
      error: error ?? this.error,
    );
  }

  @override
  AppColorsTheme lerp(ThemeExtension<AppColorsTheme>? other, double t) {
    if (other is! AppColorsTheme) return this;
    return AppColorsTheme._(
      transparent: Color.lerp(transparent, other.transparent, t)!,
      white: Color.lerp(white, other.white, t)!,
      black: Color.lerp(black, other.black, t)!,
      primary: Color.lerp(primary, other.primary, t)!,
      secondary: Color.lerp(secondary, other.secondary, t)!,
      textSecondary: Color.lerp(textSecondary, other.textSecondary, t)!,
      surface: Color.lerp(surface, other.surface, t)!,
      border: Color.lerp(border, other.border, t)!,
      disabled: Color.lerp(disabled, other.disabled, t)!,
      error: Color.lerp(error, other.error, t)!,
    );
  }
}
