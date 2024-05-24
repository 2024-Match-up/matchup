import 'package:flutter/material.dart';
import 'dart:async';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'pose/pose_detector_view.dart';

class ExerciseCameraScreen extends StatefulWidget {
  final int exerciseId;

  ExerciseCameraScreen({required this.exerciseId});

  @override
  _ExerciseCameraScreenState createState() => _ExerciseCameraScreenState();
}

class _ExerciseCameraScreenState extends State<ExerciseCameraScreen> {
  late Timer _timer;
  int _remainingTime = 10;
  bool _isExercising = false;
  late WebSocketChannel _channel;

  @override
  void initState() {
    super.initState();

    // 웹소켓 채널 초기화
    _channel = WebSocketChannel.connect(Uri.parse('ws://172.30.1.72:8000/api/v1/exercise/ws'));

    // 운동 아이디 전송
    _channel.sink.add(widget.exerciseId.toString());

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

  @override
  void dispose() {
    _timer.cancel();
    _channel.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('운동 시작하기'),
      ),
      body: _isExercising
          ? PoseDetectorView()
          : Center(
              child: Text(
                '$_remainingTime 초 후에 운동이 시작됩니다.',
                style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
              ),
            ),
    );
  }
}
