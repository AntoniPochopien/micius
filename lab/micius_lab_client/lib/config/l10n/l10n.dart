import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:micius_lab_client/config/l10n/generated/app_localizations.dart';

AppLocalizations T(BuildContext context) => AppLocalizations.of(context);

class L10n {
  static const supported = AppLocalizations.supportedLocales;

  static List<LocalizationsDelegate<dynamic>> get localizationDelegates => [
    AppLocalizations.delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ];
}
