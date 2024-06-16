// import 'package:flutter/material.dart';
// import 'exercise_camera.dart';

// class LegStretchScreen extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     double screenWidth = MediaQuery.of(context).size.width;
//     double buttonHeight = screenWidth * 0.5;
//     double fontSize = screenWidth * 0.04;
//     double largeFontSize = screenWidth * 0.05;

//     return Scaffold(
//       appBar: AppBar(
//         title: Text('다리 스트레칭'),
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
//                       '의자를 활용하여 쉽게 할 수 있는 맨몸 운동으로, 하체에 생기는 부종이나 비만을 예방합니다. '
//                       '근력을 강화하고, 혈액 순환 촉진에 도움이 되는 운동입니다. ',
//                       style: TextStyle(fontSize: fontSize),
//                       textAlign: TextAlign.left,
//                     ),
//                     SizedBox(height: 30),
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
//                       '1. 의자에 앉아 오금이 의자 끝부분에 닿지 않도록 한다. \n'
//                       '2. 몸을 앞으로 기울이지 않도록 주의하며 한 다리씩 \n'
//                       '    위로 들어올려 10초씩 버틴다. \n\n',
//                       style: TextStyle(fontSize: fontSize),
//                       textAlign: TextAlign.left,
//                     ),
//                     SizedBox(height: 0),
//                     Center(
//                       child: Text(
//                         '횟수: 10회씩 3세트',
//                         style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
//                         textAlign: TextAlign.center,
//                       ),
//                     ),
//                   ],
//                 ),
//               ),
//               SizedBox(height: 30),
//               ElevatedButton(
//                 onPressed: () {
//                   Navigator.push(
//                     context,
//                     MaterialPageRoute(builder: (context) => ExerciseCameraScreen(exerciseId: 3, exerciseName: "런지",)),
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

class LegStretchScreen extends StatefulWidget {
  @override
  _LegStretchScreenState createState() => _LegStretchScreenState();
}

class _LegStretchScreenState extends State<LegStretchScreen> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.asset('lib/assets/video/lunge.mp4')
      ..initialize().then((_) {
        setState(() {});
        _controller.play();  // 비디오 자동 재생
      });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('런지'),
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
                  MaterialPageRoute(builder: (context) => ExerciseCameraScreen(exerciseId: 3, exerciseName: "런지")),
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
