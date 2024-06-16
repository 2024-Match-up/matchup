// import 'package:flutter/material.dart';
// import 'exercise_camera.dart';
// import 'package:flutter_tts/flutter_tts.dart';

// class WaistStretchScreen extends StatefulWidget {
//   @override
//   _WaistStretchScreenState createState() => _WaistStretchScreenState();
// }

// class _WaistStretchScreenState extends State<WaistStretchScreen> {
//   late FlutterTts flutterTts;

//   @override
//   void initState() {
//     super.initState();
//     flutterTts = FlutterTts();
//   }

//   @override
//   void dispose() {
//     flutterTts.stop();
//     super.dispose();
//   }

//   Future<void> _speak(String text) async {
//     await flutterTts.setLanguage("ko-KR");
//     await flutterTts.setPitch(1.0);
//     await flutterTts.setSpeechRate(0.4); // 속도를 조절할 수 있습니다.
//     await flutterTts.speak(text);
//   }

//   @override
//   Widget build(BuildContext context) {
//     double screenWidth = MediaQuery.of(context).size.width;
//     double buttonHeight = screenWidth * 0.5;
//     double fontSize = screenWidth * 0.04;
//     double largeFontSize = screenWidth * 0.05;

//     String exerciseDescription = '방에서 쉽게 할 수 있는 맨몸 운동으로, 디스크나 인대, 관절로 전달되는 충격을 감소시킵니다. 따라서 척추의 통증을 예방하고 완화할 수 있습니다.';
//     String exerciseMethod = '1. 골반과 어깨를 수평으로 유지한다. \n2. 손을 머리 뒤로 깍지를 끼고, 팔꿈치를 수평으로 유지한다.';
//     String exerciseCount = '횟수: 좌, 우로 10회씩 3세트';

//     return Scaffold(
//       appBar: AppBar(
//         title: Text('허리 스트레칭'),
//       ),
//       body: SingleChildScrollView(
//         child: Center(
//           child: Column(
//             mainAxisAlignment: MainAxisAlignment.center,
//             children: <Widget>[
//               SizedBox(height: 25),
//               Container(
//                 margin: EdgeInsets.all(20),
//                 padding: EdgeInsets.all(20),
//                 width: double.infinity,
//                 color: Colors.grey[200],
//                 child: Column(
//                   crossAxisAlignment: CrossAxisAlignment.start,
//                   children: [
//                     Center(
//                       child: Text(
//                         '운동 설명',
//                         style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
//                         textAlign: TextAlign.center,
//                       ),
//                     ),
//                     SizedBox(height: 30),
//                     Text(
//                       exerciseDescription,
//                       style: TextStyle(fontSize: fontSize),
//                       textAlign: TextAlign.left,
//                     ),
//                     SizedBox(height: 30),
//                     ElevatedButton(
//                       onPressed: () {
//                         _speak(exerciseDescription);
//                       },
//                       child: Text('운동 설명 듣기'),
//                     ),
//                   ],
//                 ),
//               ),
//               SizedBox(height: 30),
//               Container(
//                 margin: EdgeInsets.all(20),
//                 padding: EdgeInsets.all(20),
//                 width: double.infinity,
//                 color: Colors.grey[200],
//                 child: Column(
//                   crossAxisAlignment: CrossAxisAlignment.start,
//                   children: [
//                     Center(
//                       child: Text(
//                         '운동 방법',
//                         style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
//                         textAlign: TextAlign.center,
//                       ),
//                     ),
//                     SizedBox(height: 30),
//                     Text(
//                       exerciseMethod,
//                       style: TextStyle(fontSize: fontSize),
//                       textAlign: TextAlign.left,
//                     ),
//                     SizedBox(height: 0),
//                     Center(
//                       child: Text(
//                         exerciseCount,
//                         style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
//                         textAlign: TextAlign.center,
//                       ),
//                     ),
//                     SizedBox(height: 30),
//                     ElevatedButton(
//                       onPressed: () {
//                         _speak(exerciseMethod + exerciseCount);
//                       },
//                       child: Text('운동 방법 듣기'),
//                     ),
//                   ],
//                 ),
//               ),
//               SizedBox(height: 30),
//               ElevatedButton(
//                 onPressed: () {
//                   Navigator.push(
//                     context,
//                     MaterialPageRoute(builder: (context) => ExerciseCameraScreen(exerciseId: 4, exerciseName: "허리 스트레칭",)),
//                   );
//                 },
//                 child: Text('운동하기 가기'),
//                 style: ElevatedButton.styleFrom(
//                   backgroundColor: Color(0xFFBBBBEE), // 배경색
//                   foregroundColor: Color(0xFF000000), // 텍스트색
//                   padding: EdgeInsets.symmetric(horizontal: 150, vertical: 15),
//                   textStyle: TextStyle(fontSize: fontSize * 0.8),
//                 ),
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }



import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'exercise_camera.dart';

class WaistStretchScreen extends StatefulWidget {
  @override
  _WaistStretchScreenState createState() => _WaistStretchScreenState();
}

class _WaistStretchScreenState extends State<WaistStretchScreen> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.asset('lib/assets/video/waist.mp4')
      ..initialize().then((_) {
        setState(() {});
        _controller.play();  // 비디오 자동 재생
      });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('허리 스트레칭'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Expanded(
            child: Center(  // Center 위젯 추가
              child: _controller.value.isInitialized
                ? AspectRatio(
                    aspectRatio: _controller.value.aspectRatio,
                    child: VideoPlayer(_controller),
                  )
                : Container(
                    color: Colors.grey[300],
                    child: Center(child: CircularProgressIndicator()),
                  ),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(10),
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ExerciseCameraScreen(exerciseId: 4, exerciseName: "허리 스트레칭")),
                );
              },
              child: Text('운동하기 가기'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFBBBBEE),
                foregroundColor: Color(0xFF000000),
                padding: EdgeInsets.symmetric(horizontal: 50, vertical: 15),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
