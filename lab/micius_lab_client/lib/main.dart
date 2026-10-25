import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:micius_lab_client/app/main_app.dart';
import 'package:micius_lab_client/config/di/injectable.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Future.wait([
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]),
    configureDependencies(),
  ]);
  runApp(const MainApp());
}
