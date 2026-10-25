import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import 'package:micius_lab_client/data/dto/auth/login_request_dto.dart';
import 'package:micius_lab_client/data/dto/auth/refresh_request_dto.dart';
import 'package:micius_lab_client/data/dto/auth/register_request_dto.dart';
import 'package:micius_lab_client/data/dto/auth/token_response_dto.dart';
import 'package:micius_lab_client/domain/entity/user.dart';
import 'package:retrofit/retrofit.dart';

part 'api_data_source_impl.g.dart';

@lazySingleton
@RestApi()
abstract class ApiDataSource {
  @factoryMethod
  factory ApiDataSource(@Named('apiDio') Dio dio) = _ApiDataSource;

  @POST('/register')
  Future<HttpResponse<TokenResponseDto>> register({
    @Body() required RegisterRequestDto body,
  });

  @POST('/token')
  Future<HttpResponse<TokenResponseDto>> login({
    @Body() required LoginRequestDto body,
  });

  @POST('/token/refresh')
  Future<HttpResponse<TokenResponseDto>> refresh({
    @Body() required RefreshRequestDto body,
  });

  @GET('/me')
  Future<HttpResponse<User>> getMe();
}
