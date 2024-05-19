import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Widget? icon; 

  const LoginButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.icon, 
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      icon: icon ?? SizedBox.shrink(), 
      label: Text(text),
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
      ),
    );
  }
}