import 'package:flutter/material.dart';
import 'package:micius_lab_client/utils/extensions/theme_extension.dart';

class StyledButton extends StatelessWidget {
  const StyledButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
  });

  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    final child = isLoading
        ? SizedBox(
            width: 24,
            height: 24,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              color: context.theme.white,
            ),
          )
        : Text(text, style: context.typography.buttonLarge);

    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: context.theme.primary,
        disabledBackgroundColor: context.theme.disabled,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onPressed: isLoading ? null : onPressed,
      child: SizedBox(
        width: double.infinity,
        child: Center(child: child),
      ),
    );
  }
}
