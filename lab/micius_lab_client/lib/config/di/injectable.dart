import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/config/di/injectable.config.dart';
import 'package:micius_lab_client/domain/repository/local_storage_repository.dart';

final getIt = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies() async {
  getIt.init();
  await getIt<LocalStorageRepository>().init();
}
