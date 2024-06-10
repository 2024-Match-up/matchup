import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' show join;
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:provider/provider.dart';
import '/models/UserProvider.dart'; // 수정된 경로

final String baseUrl = 'http://13.124.114.252:8000/api/v1';
// final String baseUrl = 'http://172.30.1.78:8000/api/v1';

class BodyScanScreen extends StatefulWidget {
  const BodyScanScreen({Key? key}) : super(key: key);

  @override
  State<BodyScanScreen> createState() => _BodyScanScreenState();
}

class _BodyScanScreenState extends State<BodyScanScreen> {
  late Future<void> _initializeControllerFuture;
  late CameraController _controller;
  late List<CameraDescription> _cameras;
  int _photoCount = 0;
  int _remainingTime = 8;
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _initializeControllerFuture = initializeCamera();
  }

  Future<void> initializeCamera() async {
    _cameras = await availableCameras();
    _controller = CameraController(
      _cameras.firstWhere((camera) => camera.lensDirection == CameraLensDirection.front),
      ResolutionPreset.max,
      enableAudio: false,
    );

    await _controller.initialize();
    if (mounted) {
      setState(() {});
    }
  }

  Future<void> takePicture() async {
    if (!_controller.value.isInitialized) {
      return;
    }

    try {
      final XFile file = await _controller.takePicture();
      final Directory directory = await getApplicationDocumentsDirectory();
      final String imagePath = join(directory.path, 'Photo_${DateTime.now()}.jpg');
      await File(file.path).copy(imagePath);
      setState(() {
        _photoCount++;
      });
      print('Picture saved to $imagePath');

      await _uploadImage(File(imagePath));
    } catch (e) {
      print('Error taking picture: $e');
    }
  }

  Future<void> _uploadImage(File imageFile) async {
    final uri = Uri.parse("$baseUrl/health/upload/");
    var request = http.MultipartRequest('POST', uri);
    try {
      var pic = await http.MultipartFile.fromPath(
        "file",
        imageFile.path,
        contentType: MediaType('image', 'jpeg'),
      );
      request.files.add(pic);

      final userProvider = Provider.of<UserProvider>(context, listen: false);
      final token = userProvider.accessToken;
      if (token != null) {
        print('Token: $token');
        request.headers['Authorization'] = 'Bearer $token';

        var response = await request.send();
        final respStr = await response.stream.bytesToString();

        if (response.statusCode == 200) {
          print('Image uploaded successfully');
          print('Response body: $respStr');
        } else {
          print('Failed to upload image. Status code: ${response.statusCode}');
          print('Response body: $respStr');
        }
      } else {
        print('Token is null');
      }
    } catch (e) {
      print('Error occurred: $e');
    }
  }

  void startCountdown() {
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (mounted) {
        setState(() {
          if (_remainingTime > 0) {
            _remainingTime--;
          } else {
            _timer.cancel();
            takePicture();
            _remainingTime = 8;
            if (_photoCount < 1) {
              startCountdown();
            }
          }
        });
      } else {
        timer.cancel();
      }
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
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            if (!_controller.value.isInitialized) {
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
          child: CameraPreview(_controller),
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
                        padding: EdgeInsets.all(20),
                        backgroundColor: Colors.transparent,
                        foregroundColor: Colors.black,
                      ),
                      child: Icon(
                        Icons.photo_camera,
                        size: 36,
                      ),
                    ),
                    SizedBox(height: 10),
                    Text.rich(
                      TextSpan(
                        text: '$_remainingTime 초 후에 ',
                        style: TextStyle(color: Colors.black, fontSize: 30, fontWeight: FontWeight.bold),
                        children: <TextSpan>[
                          TextSpan(
                            text: _photoCount == 0 ? '정면 촬영' : '측면 촬영',
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