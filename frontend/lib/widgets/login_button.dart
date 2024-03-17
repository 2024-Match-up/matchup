import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Widget? icon; // Add an icon field

  const LoginButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.icon, // Make the icon optional
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      icon: icon ?? SizedBox.shrink(), // Use the icon if provided, otherwise use an empty box
      label: Text(text),
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        // Define any common styles for your buttons here
      ),
    );
  }
}