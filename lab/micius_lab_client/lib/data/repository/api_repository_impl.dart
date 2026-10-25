import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/data/data_source/api_data_source_impl.dart';
import 'package:micius_lab_client/data/dto/auth/login_request_dto.dart';
import 'package:micius_lab_client/data/dto/auth/register_request_dto.dart';
import 'package:micius_lab_client/data/utils/api_repository_utils.dart';
import 'package:micius_lab_client/domain/entity/auth_token.dart';
import 'package:micius_lab_client/domain/entity/failure.dart';
import 'package:micius_lab_client/domain/entity/user.dart';
import 'package:micius_lab_client/domain/repository/api_repository.dart';

@LazySingleton(as: ApiRepository)
class ApiRepositoryImpl implements ApiRepository {
  ApiRepositoryImpl(this._apiDataSource);

  final ApiDataSource _apiDataSource;

  @override
  Future<Either<Failure, AuthToken>> login({
    required String username,
    required String password,
  }) async {
    try {
      final response = await _apiDataSource.login(
        body: LoginRequestDto(username: username, password: password),
      );
      return right(response.data.toDomain());
    } catch (e, stackTrace) {
      return left(await ApiRepositoryUtils.handleFailure(e, stackTrace));
    }
  }

  @override
  Future<Either<Failure, AuthToken>> register({
    required String username,
    required String password,
  }) async {
    try {
      final response = await _apiDataSource.register(
        body: RegisterRequestDto(username: username, password: password),
      );
      return right(response.data.toDomain());
    } catch (e, stackTrace) {
      return left(await ApiRepositoryUtils.handleFailure(e, stackTrace));
    }
  }

  @override
  Future<Either<Failure, User>> getMe() async {
    try {
      final response = await _apiDataSource.getMe();
      return right(response.data);
    } catch (e, stackTrace) {
      return left(await ApiRepositoryUtils.handleFailure(e, stackTrace));
    }
  }
}
