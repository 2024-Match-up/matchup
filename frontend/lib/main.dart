import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:camera/camera.dart';
import 'screens/login/login_screen.dart';
import 'screens/bottom_navigation_bar.dart';
import 'models/UserProvider.dart';

List<CameraDescription> cameras = [];

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  initializeDateFormatting('ko_KR', null);
  cameras = await availableCameras();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
      ],
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'match up!',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Consumer<UserProvider>(
        builder: (context, userProvider, child) {
          return userProvider.isLoggedIn
              ? BottomNavBar(accessToken: userProvider.accessToken ?? '')
              : LoginScreen();
        },
      ),
    );
  }
}


