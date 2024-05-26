import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:google_mlkit_commons/google_mlkit_commons.dart';
import 'package:matchup/main.dart'; 
import 'package:flutter/foundation.dart';

class CameraView extends StatefulWidget {
  const CameraView({
    Key? key,
    required this.customPaint,
    required this.onImage,
    this.initialDirection = CameraLensDirection.front,
  }) : super(key: key);

  final CustomPaint? customPaint;
  final Function(InputImage inputImage) onImage;
  final CameraLensDirection initialDirection;

  @override
  State<CameraView> createState() => _CameraViewState();
}

class _CameraViewState extends State<CameraView> {
  CameraController? _controller;
  int _cameraIndex = -1;
  bool _changingCameraLens = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _initializeCamera() async {
    _cameraIndex = cameras.indexWhere((camera) => camera.lensDirection == widget.initialDirection);
    if (_cameraIndex == -1) {
      _cameraIndex = 0;
    }

    _controller = CameraController(
      cameras[_cameraIndex],
      ResolutionPreset.high,
      enableAudio: false,
    );

    _controller?.initialize().then((_) {
      if (!mounted) return;
      _controller?.startImageStream(_processCameraImage);
      setState(() {});
    });
  }

  Future<void> _processCameraImage(CameraImage image) async {
    final WriteBuffer allBytes = WriteBuffer();
    for (final Plane plane in image.planes) {
      allBytes.putUint8List(plane.bytes);
    }
    final bytes = allBytes.done().buffer.asUint8List();

    final Size imageSize = Size(image.width.toDouble(), image.height.toDouble());
    final camera = cameras[_cameraIndex];
    final imageRotation = InputImageRotationValue.fromRawValue(camera.sensorOrientation) ?? InputImageRotation.rotation0deg;
    final inputImageFormat = InputImageFormatValue.fromRawValue(image.format.raw) ?? InputImageFormat.nv21;

    final planeData = image.planes.map(
      (Plane plane) {
        return InputImagePlaneMetadata(
          bytesPerRow: plane.bytesPerRow,
          height: plane.height,
          width: plane.width,
        );
      },
    ).toList();

    final inputImageData = InputImageData(
      size: imageSize,
      imageRotation: imageRotation,
      inputImageFormat: inputImageFormat,
      planeData: planeData,
    );

    final inputImage = InputImage.fromBytes(bytes: bytes, inputImageData: inputImageData);

    widget.onImage(inputImage);
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return Center(child: CircularProgressIndicator());
    }

    return Stack(
      fit: StackFit.expand,
      children: [
        CameraPreview(_controller!),
        if (widget.customPaint != null) widget.customPaint!,
      ],
    );
  }
}
