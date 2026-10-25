import 'package:flutter/material.dart';

class AppTypography extends ThemeExtension<AppTypography> {
  AppTypography._({
    required this.headerLarge,
    required this.headerMedium,
    required this.bodyLarge,
    required this.bodyMedium,
    required this.bodySmall,
    required this.buttonLarge,
  });

  factory AppTypography.light() => AppTypography._(
    headerLarge: const TextStyle(
      fontSize: 28,
      height: 34 / 28,
      fontWeight: FontWeight.w600,
    ),
    headerMedium: const TextStyle(
      fontSize: 20,
      height: 26 / 20,
      fontWeight: FontWeight.w600,
    ),
    bodyLarge: const TextStyle(
      fontSize: 16,
      height: 24 / 16,
      fontWeight: FontWeight.w400,
    ),
    bodyMedium: const TextStyle(
      fontSize: 14,
      height: 20 / 14,
      fontWeight: FontWeight.w400,
    ),
    bodySmall: const TextStyle(
      fontSize: 12,
      height: 16 / 12,
      fontWeight: FontWeight.w400,
    ),
    buttonLarge: const TextStyle(
      fontSize: 16,
      height: 24 / 16,
      fontWeight: FontWeight.w600,
    ),
  );

  final TextStyle headerLarge;
  final TextStyle headerMedium;
  final TextStyle bodyLarge;
  final TextStyle bodyMedium;
  final TextStyle bodySmall;
  final TextStyle buttonLarge;

  @override
  AppTypography copyWith({
    TextStyle? headerLarge,
    TextStyle? headerMedium,
    TextStyle? bodyLarge,
    TextStyle? bodyMedium,
    TextStyle? bodySmall,
    TextStyle? buttonLarge,
  }) {
    return AppTypography._(
      headerLarge: headerLarge ?? this.headerLarge,
      headerMedium: headerMedium ?? this.headerMedium,
      bodyLarge: bodyLarge ?? this.bodyLarge,
      bodyMedium: bodyMedium ?? this.bodyMedium,
      bodySmall: bodySmall ?? this.bodySmall,
      buttonLarge: buttonLarge ?? this.buttonLarge,
    );
  }

  @override
  AppTypography lerp(ThemeExtension<AppTypography>? other, double t) {
    if (other is! AppTypography) return this;
    return AppTypography._(
      headerLarge: TextStyle.lerp(headerLarge, other.headerLarge, t)!,
      headerMedium: TextStyle.lerp(headerMedium, other.headerMedium, t)!,
      bodyLarge: TextStyle.lerp(bodyLarge, other.bodyLarge, t)!,
      bodyMedium: TextStyle.lerp(bodyMedium, other.bodyMedium, t)!,
      bodySmall: TextStyle.lerp(bodySmall, other.bodySmall, t)!,
      buttonLarge: TextStyle.lerp(buttonLarge, other.buttonLarge, t)!,
    );
  }
}
