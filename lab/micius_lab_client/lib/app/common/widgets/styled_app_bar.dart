import 'package:flutter/material.dart';
import 'package:micius_lab_client/utils/extensions/theme_extension.dart';

class StyledAppBar extends StatelessWidget implements PreferredSizeWidget {
  const StyledAppBar({super.key, this.title});

  final String? title;

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    final title = this.title;
    return AppBar(
      title: title == null
          ? null
          : Text(title, style: context.typography.headerMedium),
      backgroundColor: context.theme.white,
      foregroundColor: context.theme.black,
      elevation: 0,
      centerTitle: false,
      notificationPredicate: (_) => false,
    );
  }
}
