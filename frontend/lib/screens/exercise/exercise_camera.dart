import 'package:flutter/material.dart';
import 'package:matchup/screens/exercise/pose/pose_painter.dart';
import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'pose/pose_detector_view.dart';
import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';
import 'package:matchup/models/UserProvider.dart';
import 'package:provider/provider.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'dart:collection'; // 큐 사용을 위해 추가
import 'score_modal.dart';

class ExerciseCameraScreen extends StatefulWidget {
  final int exerciseId;
  final String exerciseName;

  ExerciseCameraScreen({required this.exerciseId, required this.exerciseName});

  @override
  _ExerciseCameraScreenState createState() => _ExerciseCameraScreenState();
}

class _ExerciseCameraScreenState extends State<ExerciseCameraScreen> {
  late Timer _timer;
  late Timer _coordinateTimer;
  int _remainingTime = 10;  // 10초 타이머 설정
  bool _isExercising = false;
  late WebSocketChannel _channel;
  List<Pose> _detectedPoses = [];
  String feedback = "";
  int realCount = 0;
  int sets = 0;
  bool _isWebSocketConnected = false;

  FlutterTts flutterTts = FlutterTts();
  Queue<String> ttsQueue = Queue<String>();
  String lastSpokenFeedback = "";
  bool isSpeaking = false;

  @override
  void initState() {
    super.initState();

    _initializeTTS();

    _connectWebSocket();
    _startTimer();
  }

  void _initializeTTS() {
    flutterTts.setLanguage('ko-KR').catchError((error) {
      print("Error setting language: $error");
    }); // TTS 언어 설정
    flutterTts.setSpeechRate(0.5); // 말하는 속도 설정

    flutterTts.setCompletionHandler(() {
      setState(() {
        isSpeaking = false;
        if (ttsQueue.isNotEmpty) {
          _speak();
        }
      });
    });
  }

  void _connectWebSocket() {
    try {
      _channel = WebSocketChannel.connect(
        Uri.parse('ws://13.124.114.252:8000/api/v1/exercise/ws'),
        // Uri.parse('ws://10.254.3.138:8000/api/v1/exercise/ws'),
      );

      final userProvider = Provider.of<UserProvider>(context, listen: false);
      String? accessToken = userProvider.accessToken;
      _channel.sink.add(jsonEncode({
        "exercise_id": widget.exerciseId,
        "access_token": accessToken,
      }));

      _channel.stream.listen(
        (event) {
          print('WebSocket event: $event');
          try {
            final data = jsonDecode(event);

            if (data.containsKey('final_score') && data.containsKey('total_count')) {
              // final int? totalCount = data['total_count'] is int ? data['total_count'] : null;
              // final double? finalScore = data['final_score'] is double ? data['final_score'] : null;
              int? totalCount = data['total_count'] ?? 0;
              double? finalScore = data['final_score'] ?? 0.0;

              if (totalCount != null && finalScore != null && totalCount >= 4) {
                showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return ScoreModal(
                      score: finalScore,
                      exerciseName: widget.exerciseName,
                    );
                  },
                );
              }
            } else {
              setState(() {
                feedback = data['feedback'] ?? '';
                realCount = data['counter'] ?? 0;
                sets = data['sets'] ?? 0;
                print('Updated realCount: $realCount, sets: $sets');
                if (feedback.isNotEmpty && feedback != lastSpokenFeedback && !ttsQueue.contains(feedback)) {
                  ttsQueue.add(feedback);
                  if (!isSpeaking) {
                    _speak();
                  }
                }
              });
            }
          } catch (e) {
            print('Error parsing JSON: $e');
          }
        },
        onError: (error) {
          print('WebSocket error: $error');
          setState(() {
            _isWebSocketConnected = false;
          });
        },
        onDone: () {
          print('WebSocket connection closed.');
          setState(() {
            _isWebSocketConnected = false;
          });
        },
      );

      setState(() {
        _isWebSocketConnected = true;
      });

    } catch (e) {
      print('WebSocket connection failed: $e');
    }
  }

  void _startTimer() {
    _timer = Timer.periodic(Duration(seconds: 1), (Timer timer) {
      if (_remainingTime > 0) {
        setState(() {
          _remainingTime--;
        });
      } else {
        setState(() {
          _isExercising = true;
          _timer.cancel();
          _sendCoordinatesPeriodically();
        });
      }
    });
  }

  Future<void> _speak() async {
    if (ttsQueue.isNotEmpty) {
      String message = ttsQueue.removeFirst();
      setState(() {
        isSpeaking = true;
        lastSpokenFeedback = message;
      });
      await flutterTts.speak(message);
    }
  }

  @override
  void dispose() {
    _timer.cancel();
    if (_coordinateTimer.isActive) {
      _coordinateTimer.cancel();
    }
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
          ? Stack(
              children: [
                Positioned.fill(
                  child: PoseDetectorView(
                    onPosesDetected: (poses) {
                      setState(() {
                        _detectedPoses = poses;
                      });
                    },
                  ),
                ),
                Positioned(
                  top: 16,
                  left: 16,
                  child: Text(
                    'Count: $realCount',
                    style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold, color: Colors.black),
                  ),
                ),
                Positioned(
                  top: 16,
                  right: 16,
                  child: Text(
                    'Sets: $sets',
                    style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold, color: Colors.black),
                  ),
                ),
                Positioned(
                  bottom: 16,
                  left: 16,
                  right: 16,
                  child: Text(
                    'Feedback: $feedback',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.black),
                  ),
                ),
              ],
            )
          : Center(
              child: Text(
                '$_remainingTime 초 후에 운동이 시작됩니다.',
                style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
              ),
            ),
    );
  }

  void _sendCoordinatesPeriodically() {
    _coordinateTimer = Timer.periodic(Duration(milliseconds: 300), (Timer timer) {
      if (_isExercising && _isWebSocketConnected) {
        List<Offset> coordinates = [];
        switch (widget.exerciseId) {
          case 1:
            coordinates = PosePainter.getNeckCoordinates(_detectedPoses);
            break;
          case 2:
            coordinates = PosePainter.getSquatCoordinates(_detectedPoses);
            break;
          case 3:
            coordinates = PosePainter.getLegCoordinates(_detectedPoses);
            break;
          case 4:
            coordinates = PosePainter.getWaistCoordinates(_detectedPoses);
            break;
          default:
            coordinates = [];
        }
        _channel.sink.add(jsonEncode({
          "coordinates": coordinates.map((offset) => customEncode(offset)).toList(),
        }));
        print('Coordinates: $coordinates');
      } else {
        timer.cancel();
      }
    });
  }

  dynamic customEncode(dynamic item) {
    if (item is Offset) {
      return {'dx': item.dx, 'dy': item.dy};
    }
    return item;
  }
}
