import 'package:flutter/material.dart';
import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';

import 'coordinates_translator.dart';

class PosePainter extends CustomPainter {
  PosePainter(this.poses, this.absoluteImageSize, this.rotation);

  final List<Pose> poses;
  final Size absoluteImageSize;
  final InputImageRotation rotation;

  @override
  void paint(Canvas canvas, Size size) {
    // 초록: 33개의 관절 포인트(랜드마크) 색깔
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 10.0
      ..color = Colors.white;

    // 파랑: 왼쪽 선 색깔(왼팔~왼다리)
    final leftPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0
      ..color = Colors.blueAccent;

    // 파랑: 오른쪽 선 색깔(오른팔~오른다리)
    final rightPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0
      ..color = Colors.blueAccent;

    // 추출된 관절 포인트 갯수만큼 점 그리기
    for (final pose in poses) {
      pose.landmarks.forEach((_, landmark) {
        canvas.drawCircle(
            Offset(
              translateX(landmark.x, rotation, size, absoluteImageSize),
              translateY(landmark.y, rotation, size, absoluteImageSize),
            ),
            1,
            paint);
      });

      // 점1과 점2를 선으로 이어주는 함수(랜드마크 타입1, 랜드마크 타입2, 선 색깔 타입)
      void paintLine(
          PoseLandmarkType type1, PoseLandmarkType type2, Paint paintType) {
        final PoseLandmark joint1 = pose.landmarks[type1]!;
        final PoseLandmark joint2 = pose.landmarks[type2]!;
        canvas.drawLine(
            Offset(translateX(joint1.x, rotation, size, absoluteImageSize),
                translateY(joint1.y, rotation, size, absoluteImageSize)),
            Offset(translateX(joint2.x, rotation, size, absoluteImageSize),
                translateY(joint2.y, rotation, size, absoluteImageSize)),
            paintType);
      }

      //Draw arms
      paintLine(
          PoseLandmarkType.leftShoulder, PoseLandmarkType.leftElbow, leftPaint);
      paintLine(
          PoseLandmarkType.leftElbow, PoseLandmarkType.leftWrist, leftPaint);
      paintLine(PoseLandmarkType.rightShoulder, PoseLandmarkType.rightElbow,
          rightPaint);
      paintLine(
          PoseLandmarkType.rightElbow, PoseLandmarkType.rightWrist, rightPaint);

      //Draw Body
      paintLine(
          PoseLandmarkType.leftShoulder, PoseLandmarkType.leftHip, leftPaint);
      paintLine(PoseLandmarkType.rightShoulder, PoseLandmarkType.rightHip,
          rightPaint);

      //Draw legs
      paintLine(PoseLandmarkType.leftHip, PoseLandmarkType.leftKnee, leftPaint);
      paintLine(
          PoseLandmarkType.leftKnee, PoseLandmarkType.leftAnkle, leftPaint);
      paintLine(
          PoseLandmarkType.rightHip, PoseLandmarkType.rightKnee, rightPaint);
      paintLine(
          PoseLandmarkType.rightKnee, PoseLandmarkType.rightAnkle, rightPaint);
    }
  }

  // 허리 좌표를 반환하는 함수
  static List<Offset> getWaistCoordinates(List<Pose> poses) {
    final List<Offset> coordinates = [];
    for (final pose in poses) {
      coordinates.add(
        Offset(
          pose.landmarks[PoseLandmarkType.leftShoulder]!.x,
          pose.landmarks[PoseLandmarkType.leftShoulder]!.y,
        ),
      );
      coordinates.add(
        Offset(
          pose.landmarks[PoseLandmarkType.rightShoulder]!.x,
          pose.landmarks[PoseLandmarkType.rightShoulder]!.y,
        ),
      );
      coordinates.add(
        Offset(
          pose.landmarks[PoseLandmarkType.leftElbow]!.x,
          pose.landmarks[PoseLandmarkType.leftElbow]!.y,
        ),
      );
      coordinates.add(
        Offset(
          pose.landmarks[PoseLandmarkType.rightElbow]!.x,
          pose.landmarks[PoseLandmarkType.rightElbow]!.y,
        ),
      );
    }
    return coordinates;
  }

  @override
  bool shouldRepaint(covariant PosePainter oldDelegate) {
    return oldDelegate.absoluteImageSize != absoluteImageSize ||
        oldDelegate.poses != poses;
  }
}

