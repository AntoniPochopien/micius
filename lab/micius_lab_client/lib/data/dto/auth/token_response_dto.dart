import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:micius_lab_client/domain/entity/auth_token.dart';

part 'token_response_dto.freezed.dart';
part 'token_response_dto.g.dart';

@freezed
abstract class TokenResponseDto with _$TokenResponseDto {
  const TokenResponseDto._();

  const factory TokenResponseDto({
    @JsonKey(name: 'access_token') required String accessToken,
    @JsonKey(name: 'refresh_token') required String refreshToken,
    @JsonKey(name: 'token_type') @Default('bearer') String tokenType,
  }) = _TokenResponseDto;

  factory TokenResponseDto.fromJson(Map<String, dynamic> json) =>
      _$TokenResponseDtoFromJson(json);

  AuthToken toDomain() => AuthToken(
    accessToken: accessToken,
    refreshToken: refreshToken,
  );
}
