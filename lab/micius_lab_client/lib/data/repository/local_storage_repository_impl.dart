import 'dart:convert';
import 'dart:ui';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:hive_ce_flutter/hive_ce_flutter.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/domain/repository/local_storage_repository.dart';

enum _Key { languageCode, encryptionKey, accessToken, refreshToken }

@LazySingleton(as: LocalStorageRepository)
class LocalStorageRepositoryImpl implements LocalStorageRepository {
  static const String _boxName = 'micius_lab_client';
  late final Box _box;
  late final FlutterSecureStorage _secureStorage;

  @override
  Future<void> init() async {
    await Hive.initFlutter();
    _secureStorage = const FlutterSecureStorage();
    _box = await _openEncryptedBox();
  }

  Future<Box> _openEncryptedBox() async {
    final encryptionKey = await _getOrCreateEncryptionKey();
    try {
      return await Hive.openBox(
        _boxName,
        encryptionCipher: HiveAesCipher(encryptionKey),
      );
    } catch (_) {
      await Hive.deleteBoxFromDisk(_boxName);
      await _secureStorage.delete(key: _Key.encryptionKey.name);
      final freshKey = await _getOrCreateEncryptionKey();
      return Hive.openBox(_boxName, encryptionCipher: HiveAesCipher(freshKey));
    }
  }

  Future<List<int>> _getOrCreateEncryptionKey() async {
    final storedKey = await _secureStorage.read(key: _Key.encryptionKey.name);
    if (storedKey != null) {
      return base64Url.decode(storedKey);
    }
    final newKey = Hive.generateSecureKey();
    await _secureStorage.write(
      key: _Key.encryptionKey.name,
      value: base64UrlEncode(newKey),
    );
    return newKey;
  }

  @override
  Locale? getLocale() {
    final languageCode = _box.get(_Key.languageCode.name);
    if (languageCode != null) {
      return Locale(languageCode as String);
    }
    return null;
  }

  @override
  Future<void> setLocale(Locale locale) async =>
      _box.put(_Key.languageCode.name, locale.languageCode);

  @override
  Future<String?> getAccessToken() async =>
      _secureStorage.read(key: _Key.accessToken.name);

  @override
  Future<void> setAccessToken(String accessToken) async =>
      _secureStorage.write(key: _Key.accessToken.name, value: accessToken);

  @override
  Future<String?> getRefreshToken() async =>
      _secureStorage.read(key: _Key.refreshToken.name);

  @override
  Future<void> setRefreshToken(String refreshToken) async =>
      _secureStorage.write(key: _Key.refreshToken.name, value: refreshToken);

  @override
  Future<void> clear() async {
    await _secureStorage.deleteAll();
    await _box.clear();
  }
}
