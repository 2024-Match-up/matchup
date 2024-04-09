import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' show join;

class BodyScanScreen extends StatefulWidget {
  const BodyScanScreen({Key? key}) : super(key: key);

  @override
  State<BodyScanScreen> createState() => CameraAppState();
}

class CameraAppState extends State<BodyScanScreen> {
  late Future<void> _initializeControllerFuture;
  late CameraController? _controller;
  late List<CameraDescription> _cameras;
  int _photoCount = 0;
  int _remainingTime = 5;
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _initializeControllerFuture = initializeCamera();
    _timer = Timer(Duration.zero, () {}); // Initialize _timer with a dummy Timer
  }


  Future<void> initializeCamera() async {
    _cameras = await availableCameras();
    _controller = CameraController(
      _cameras.firstWhere((camera) => camera.lensDirection == CameraLensDirection.front),
      ResolutionPreset.max,
      enableAudio: false,
    );

    try {
      await _controller!.initialize();
      setState(() {});
    } catch (e) {
      print('Failed to initialize camera: $e');
    }
  }

  Future<void> takePicture() async {
    if (_controller == null || !_controller!.value.isInitialized) {
      return;
    }

    try {
      final XFile file = await _controller!.takePicture();
      final Directory directory = await getApplicationDocumentsDirectory();
      final String imagePath = join(directory.path, 'Photo_${DateTime.now()}.jpg');
      await File(file.path).copy(imagePath);
      setState(() {
        _photoCount++;
      });
      print('Picture saved to $imagePath');
    } catch (e) {
      print('Error taking picture: $e');
    }
  }

  void startCountdown() {
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        if (_remainingTime > 0) {
          _remainingTime--;
        } else {
          _timer.cancel();
          takePicture();
          _remainingTime = 5;
          _timer = Timer.periodic(Duration(seconds: 1), (timer) {
            setState(() {
              if (_remainingTime > 0) {
                _remainingTime--;
              } else {
                _timer.cancel();
                takePicture();
              }
            });
          });
        }
      });
    });
  }

  @override
  void dispose() {
    _controller?.dispose();
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            if (_controller == null || !_controller!.value.isInitialized) {
              return Center(child: Text('Error: Failed to initialize camera.'));
            }
            return buildCameraPreview();
          } else {
            return Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }

  Widget buildCameraPreview() {
    return Stack(
      children: [
        Positioned.fill(
          child: CameraPreview(_controller!),
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: Padding(
            padding: const EdgeInsets.all(15.0),
            child: SizedBox(
              width: 500,
              height: 150,
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.5),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    SizedBox(height: 10),
                    ElevatedButton(
                      onPressed: _photoCount < 2 ? startCountdown : null,
                      style: ElevatedButton.styleFrom(
                        shape: CircleBorder(),
                        padding: EdgeInsets.all(20), // Increase icon size
                        backgroundColor: Colors.transparent, // Remove button background color
                        foregroundColor: Colors.black, // Set button text color
                      ),
                      child: Icon(
                        Icons.photo_camera,
                        size: 36, // Increase icon size
                      ),
                    ),
                    SizedBox(height: 10), // Add space between icon and text
                    Text.rich(
                      _photoCount == 0
                          ? TextSpan(
                              text: '$_remainingTime 초 후에 ',
                              style: TextStyle(color: Colors.white, fontSize: 26),
                              children: <TextSpan>[
                                TextSpan(
                                  text: '정면 촬영',
                                  style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
                                ),
                                TextSpan(
                                  text: '을 시작합니다.',
                                ),
                              ],
                            )
                          : TextSpan(
                              text: '$_remainingTime 초 후에 ',
                              style: TextStyle(color: Colors.white, fontSize: 26),
                              children: <TextSpan>[
                                TextSpan(
                                  text: '측면 촬영',
                                  style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
                                ),
                                TextSpan(
                                  text: '을 시작합니다.',
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          );
        }
}
