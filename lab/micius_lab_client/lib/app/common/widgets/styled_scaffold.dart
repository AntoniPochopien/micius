import 'package:flutter/material.dart';
import 'package:micius_lab_client/utils/extensions/theme_extension.dart';

class StyledScaffold extends StatelessWidget {
  const StyledScaffold({
    super.key,
    this.body,
    this.appBar,
    this.scrollBody = false,
    this.padding,
    this.bottomNavigationBar,
  });

  final Widget? body;
  final PreferredSizeWidget? appBar;
  final bool scrollBody;
  final EdgeInsets? padding;
  final Widget? bottomNavigationBar;

  static const _bottomContentPadding = 20.0;

  @override
  Widget build(BuildContext context) {
    final hasBottomNav = bottomNavigationBar != null;
    final resolvedPadding =
        padding ?? const EdgeInsets.symmetric(horizontal: 20);
    final content = Padding(
      padding: hasBottomNav
          ? resolvedPadding
          : resolvedPadding.add(
              const EdgeInsets.only(bottom: _bottomContentPadding),
            ),
      child: body,
    );

    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        appBar: appBar,
        bottomNavigationBar: bottomNavigationBar,
        backgroundColor: context.theme.surface,
        body: SafeArea(
          bottom: !hasBottomNav,
          child: scrollBody ? SingleChildScrollView(child: content) : content,
        ),
      ),
    );
  }
}
