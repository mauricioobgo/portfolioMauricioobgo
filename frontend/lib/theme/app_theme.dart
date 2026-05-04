import 'package:flutter/material.dart';

class AppPalette {
  static const background = Color(0xFF071018);
  static const backgroundAlt = Color(0xFF0B1722);
  static const panel = Color(0xFF0E1E2B);
  static const panelSoft = Color(0xFF132535);
  static const border = Color(0xFF214357);
  static const primary = Color(0xFF12F7A0);
  static const primarySoft = Color(0xFF65FFD1);
  static const cyan = Color(0xFF4DBDFF);
  static const warning = Color(0xFFFFD166);
  static const text = Color(0xFFF3FBFF);
  static const textMuted = Color(0xFF9BB5C4);
}

ThemeData buildAppTheme() {
  final base = ThemeData.dark(useMaterial3: true);
  const surface = AppPalette.panel;
  const card = AppPalette.panelSoft;

  return base.copyWith(
    scaffoldBackgroundColor: AppPalette.background,
    colorScheme: const ColorScheme.dark(
      brightness: Brightness.dark,
      primary: AppPalette.primary,
      onPrimary: AppPalette.background,
      secondary: AppPalette.cyan,
      onSecondary: AppPalette.background,
      surface: surface,
      onSurface: AppPalette.text,
      error: Color(0xFFFF6B6B),
      onError: AppPalette.text,
    ),
    textTheme: base.textTheme.apply(
      fontFamily: 'Poppins',
      bodyColor: AppPalette.text,
      displayColor: AppPalette.text,
    ),
    cardTheme: CardThemeData(
      color: card,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(28),
        side: const BorderSide(color: AppPalette.border),
      ),
      margin: EdgeInsets.zero,
    ),
    chipTheme: base.chipTheme.copyWith(
      backgroundColor: AppPalette.panelSoft,
      disabledColor: AppPalette.panelSoft,
      selectedColor: AppPalette.primary.withValues(alpha: 0.16),
      side: const BorderSide(color: AppPalette.border),
      labelStyle: const TextStyle(
        color: AppPalette.text,
        fontFamily: 'IBMPlexMono',
        fontSize: 12,
        fontWeight: FontWeight.w500,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(999),
      ),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Colors.transparent,
      foregroundColor: AppPalette.text,
      elevation: 0,
      surfaceTintColor: Colors.transparent,
    ),
    dividerColor: AppPalette.border,
    splashFactory: InkRipple.splashFactory,
  );
}
