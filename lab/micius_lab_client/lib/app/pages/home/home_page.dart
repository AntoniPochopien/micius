import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:micius_lab_client/app/common/widgets/styled_app_bar.dart';
import 'package:micius_lab_client/app/common/widgets/styled_button.dart';
import 'package:micius_lab_client/app/common/widgets/styled_scaffold.dart';
import 'package:micius_lab_client/app/cubits/auth_cubit/auth_cubit.dart';
import 'package:micius_lab_client/config/l10n/l10n.dart';
import 'package:micius_lab_client/domain/entity/failure.dart';
import 'package:micius_lab_client/utils/extensions/theme_extension.dart';

@RoutePage()
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return StyledScaffold(
      appBar: StyledAppBar(title: T(context).homeTitle),
      body: BlocBuilder<AuthCubit, AuthState>(
        builder: (context, state) {
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                T(context).appName,
                style: context.typography.headerLarge,
              ),
              const SizedBox(height: 12),
              Text(
                state.map(
                  loading: (_) => '…',
                  unauthenticated: (_) => T(context).unauthorized,
                  authenticated: (value) => value.user.username,
                  error: (value) => value.failure.errorMessage(context),
                ),
                style: context.typography.bodyLarge.copyWith(
                  color: context.theme.textSecondary,
                ),
              ),
              const Spacer(),
              state.maybeMap(
                authenticated: (_) => StyledButton(
                  text: T(context).logout,
                  onPressed: () => context.read<AuthCubit>().logout(),
                ),
                orElse: () => const SizedBox.shrink(),
              ),
            ],
          );
        },
      ),
    );
  }
}
