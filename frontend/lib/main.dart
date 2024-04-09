import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:matchup/screens/login/login_screen.dart';
import 'package:matchup/screens/camera/body_scan.dart'; 
import 'package:intl/intl.dart';
import 'package:intl/date_symbol_data_local.dart';



Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  initializeDateFormatting('ko_KR', null);

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'match up!',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginScreen(),
    );
  }
}
