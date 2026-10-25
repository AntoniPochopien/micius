import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:micius_lab_client/app/cubits/auth_cubit/auth_cubit.dart';
import 'package:micius_lab_client/app/cubits/locale_cubit/locale_cubit.dart';
import 'package:micius_lab_client/config/di/injectable.dart';
import 'package:micius_lab_client/config/l10n/l10n.dart';
import 'package:micius_lab_client/config/routing/app_router.dart';
import 'package:micius_lab_client/config/theme/app_theme.dart';

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    final router = getIt<AppRouter>();
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => getIt<LocaleCubit>()..init()),
        BlocProvider(create: (_) => getIt<AuthCubit>()..fetchUser()),
      ],
      child: BlocBuilder<LocaleCubit, LocaleState>(
        builder: (context, localeState) => GestureDetector(
          behavior: HitTestBehavior.opaque,
          onTap: FocusScope.of(context).unfocus,
          child: MaterialApp.router(
            localizationsDelegates: L10n.localizationDelegates,
            supportedLocales: L10n.supported,
            locale: localeState.locale,
            theme: AppTheme.light().toThemeData(),
            routerConfig: router.config(
              navigatorObservers: () => [AutoRouteObserver()],
            ),
            builder: (context, child) => MediaQuery(
              data: MediaQuery.of(
                context,
              ).copyWith(textScaler: TextScaler.noScaling),
              child: child!,
            ),
          ),
        ),
      ),
    );
  }
}
