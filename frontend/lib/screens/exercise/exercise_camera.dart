import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';

class ExerciseCameraScreen extends StatefulWidget {
  @override
  _ExerciseCameraScreenState createState() => _ExerciseCameraScreenState();
}

class _ExerciseCameraScreenState extends State<ExerciseCameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  late Timer _timer;
  int _remainingTime = 15; 
  bool _isExercising = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
    _timer = Timer.periodic(Duration(seconds: 1), (Timer timer) {
      if (_remainingTime > 0) {
        setState(() {
          _remainingTime--;
        });
      } else {
        setState(() {
          _isExercising = true;
          _timer.cancel(); 
        });
      }
    });
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    _controller = CameraController(
      cameras.firstWhere(
        (camera) => camera.lensDirection == CameraLensDirection.front,
      ),
      ResolutionPreset.high,
    );

    _initializeControllerFuture = _controller.initialize().catchError((Object e) {
      if (!mounted) {
        return;
      }
      print('Camera initialization error: $e');
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('운동 시작하기'),
      ),
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            if (!_controller.value.isInitialized) {
              return Text('Camera Initialization Failed');
            }
            return Column(
              children: [
                Expanded(
                  child: Container(
                    width: MediaQuery.of(context).size.width, 
                    child: CameraPreview(_controller)
                  ),
                ),
                buildExerciseInfo(context), 
              ],
            );
          } else {
            return Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }

  Widget buildExerciseInfo(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double fontSize = screenWidth * 0.04;

    return Column(
      children: [
        if (!_isExercising)
          Padding(
            padding: EdgeInsets.all(screenWidth * 0.02),
            child: Text(
              ' $_remainingTime 초후에 운동이 시작됩니다.',
              style: TextStyle(fontSize: fontSize, fontWeight: FontWeight.bold),
            ),
          ),
        if (_isExercising)
          Padding(
            padding: EdgeInsets.all(screenWidth * 0.02),
            child: Text(
              'Exercise in progress...',
              style: TextStyle(fontSize: fontSize, fontWeight: FontWeight.bold),
            ),
          ),
      ],
    );
  }
}
