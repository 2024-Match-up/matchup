import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  void _initCamera() async {
    // 사용 가능한 카메라 목록을 가져옵니다.
    final cameras = await availableCameras();

    // 특정 카메라를 선택합니다. 일반적으로 후면 카메라를 사용합니다.
    final firstCamera = cameras.firstWhere(
      (camera) => camera.lensDirection == CameraLensDirection.back,
    );

    // 카메라 컨트롤러를 초기화합니다.
    _controller = CameraController(
      firstCamera,
      ResolutionPreset.high,
      imageFormatGroup: ImageFormatGroup.yuv420,
    );

    // 컨트롤러를 통해 카메라를 초기화합니다.
    _initializeControllerFuture = _controller!.initialize().then((_) {
      // 컨트롤러 초기화가 완료되면, 화면을 갱신합니다.
      if (!mounted) return;
      setState(() {});
    });
  }

  @override
  void dispose() {
    // 위젯이 메모리에서 제거될 때, 컨트롤러를 해제합니다.
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // 컨트롤러 초기화를 기다립니다.
    if (_controller == null || !_controller!.value.isInitialized) {
      return Center(child: CircularProgressIndicator());
    }

    // 카메라 미리보기를 표시하는 위젯을 반환합니다.
    return Scaffold(
      appBar: AppBar(title: Text('Camera Preview')),
      // FutureBuilder를 사용하여 카메라의 초기화를 비동기적으로 기다립니다.
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // 초기화가 완료되면, 카메라 미리보기를 보여줍니다.
            return CameraPreview(_controller!);
          } else {
            // 그렇지 않다면, 진행 표시기를 보여줍니다.
            return Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
