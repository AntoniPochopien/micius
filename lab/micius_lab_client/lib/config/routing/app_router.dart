import 'package:auto_route/auto_route.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/app/pages/home/home_page.dart';

part 'app_router.gr.dart';

@LazySingleton()
@AutoRouterConfig(replaceInRouteName: 'Page,Route')
class AppRouter extends RootStackRouter {
  @override
  List<AutoRoute> get routes => [
    AutoRoute(page: HomeRoute.page, initial: true),
  ];
}
