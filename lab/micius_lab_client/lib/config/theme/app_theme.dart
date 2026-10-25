import 'package:flutter/material.dart';
import 'package:micius_lab_client/config/theme/app_colors.dart';
import 'package:micius_lab_client/config/theme/app_typography.dart';

class AppTheme {
  AppTheme._({required this.colors, required this.typography});

  factory AppTheme.light() {
    final colors = AppColorsTheme.light();
    return AppTheme._(colors: colors, typography: AppTypography.light());
  }

  final AppColorsTheme colors;
  final AppTypography typography;

  ThemeData toThemeData() {
    final base = ThemeData(useMaterial3: true);

    return base.copyWith(
      colorScheme: ColorScheme.light(
        primary: colors.primary,
        onPrimary: colors.white,
        secondary: colors.secondary,
        onSecondary: colors.black,
        surface: colors.surface,
        onSurface: colors.black,
        error: colors.error,
        onError: colors.white,
      ),
      scaffoldBackgroundColor: colors.white,
      textTheme: base.textTheme.apply(
        bodyColor: colors.black,
        displayColor: colors.black,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          foregroundColor: colors.white,
          backgroundColor: colors.primary,
          disabledForegroundColor: colors.textSecondary,
          disabledBackgroundColor: colors.disabled,
          textStyle: typography.buttonLarge,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        ),
      ),
      extensions: [colors, typography],
    );
  }
}
