// import 'package:flutter/cupertino.dart';
// import 'package:flutter/material.dart';
// import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';
// import 'pose_painter.dart';
// import 'carema_view.dart';

// class PoseDetectorView extends StatefulWidget {
//   const PoseDetectorView({Key? key}) : super(key: key);

//   @override
//   State<PoseDetectorView> createState() => _PoseDetectorViewState();
// }

// class _PoseDetectorViewState extends State<PoseDetectorView> {
//   final PoseDetector _poseDetector = PoseDetector(options: PoseDetectorOptions());
//   bool _canProcess = true;
//   bool _isBusy = false;
//   CustomPaint? _customPaint;

//   @override
//   void dispose() {
//     _canProcess = false;
//     _poseDetector.close();
//     super.dispose();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return CameraView(
//       customPaint: _customPaint,
//       onImage: (inputImage) {
//         processImage(inputImage);
//       },
//     );
//   }

//   Future<void> processImage(InputImage inputImage) async {
//     if (!_canProcess || _isBusy) return;
//     _isBusy = true;

//     final poses = await _poseDetector.processImage(inputImage);

//     if (inputImage.inputImageData?.size != null &&
//         inputImage.inputImageData?.imageRotation != null) {
//       final painter = PosePainter(
//         poses,
//         inputImage.inputImageData!.size,
//         inputImage.inputImageData!.imageRotation,
//       );
//       _customPaint = CustomPaint(painter: painter);
//     } else {
//       _customPaint = null;
//     }

//     _isBusy = false;
//     if (mounted) {
//       setState(() {});
//     }
//   }
// }

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';
import 'pose_painter.dart';
import 'carema_view.dart';

typedef PosesCallback = void Function(List<Pose> poses);

class PoseDetectorView extends StatefulWidget {
  
  final PosesCallback onPosesDetected;

  const PoseDetectorView({Key? key, required this.onPosesDetected}) : super(key: key);

  @override
  State<PoseDetectorView> createState() => _PoseDetectorViewState();
}

class _PoseDetectorViewState extends State<PoseDetectorView> {
  final PoseDetector _poseDetector = PoseDetector(options: PoseDetectorOptions());
  bool _canProcess = true;
  bool _isBusy = false;
  CustomPaint? _customPaint;

  @override
  void dispose() {
    _canProcess = false;
    _poseDetector.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return CameraView(
      customPaint: _customPaint,
      onImage: (inputImage) {
        processImage(inputImage);
      },
    );
  }

  Future<void> processImage(InputImage inputImage) async {
    if (!_canProcess || _isBusy) return;
    _isBusy = true;

    final poses = await _poseDetector.processImage(inputImage);

    if (inputImage.inputImageData?.size != null &&
        inputImage.inputImageData?.imageRotation != null) {
      final painter = PosePainter(
        poses,
        inputImage.inputImageData!.size,
        inputImage.inputImageData!.imageRotation,
      );
      _customPaint = CustomPaint(painter: painter);
    } else {
      _customPaint = null;
    }

    // Invoke the callback function and pass the detected poses
    widget.onPosesDetected(poses);

    _isBusy = false;
    if (mounted) {
      setState(() {});
    }
  }
}
