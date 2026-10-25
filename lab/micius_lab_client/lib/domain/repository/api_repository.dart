import 'package:dartz/dartz.dart';
import 'package:micius_lab_client/domain/entity/auth_token.dart';
import 'package:micius_lab_client/domain/entity/failure.dart';
import 'package:micius_lab_client/domain/entity/user.dart';

abstract class ApiRepository {
  Future<Either<Failure, AuthToken>> login({
    required String username,
    required String password,
  });

  Future<Either<Failure, AuthToken>> register({
    required String username,
    required String password,
  });

  Future<Either<Failure, User>> getMe();
}
