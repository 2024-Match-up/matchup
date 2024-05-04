import 'package:flutter/material.dart';
import 'exercise_camera.dart';

class WaistStretchScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double buttonHeight = screenWidth * 0.5;
    double fontSize = screenWidth * 0.05;

    return Scaffold(
      appBar: AppBar(
        title: Text('목 스트레칭'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              margin: EdgeInsets.all(20),
              padding: EdgeInsets.all(20),
              width: double.infinity,
              height: buttonHeight, 
              color: Colors.grey[200],
              child: Center(
                child: Text(
                  '텍스트 버튼 1',
                  style: TextStyle(fontSize: fontSize), 
                ),
              ),
            ),
            Container(
              margin: EdgeInsets.all(20),
              padding: EdgeInsets.all(20),
              width: double.infinity,
              height: buttonHeight, 
              color: Colors.grey[200],
              child: Center(
                child: Text(
                  '텍스트 버튼 2',
                  style: TextStyle(fontSize: fontSize), 
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => ExerciseCameraScreen()), 
              );
            },
              child: Text('운동하기 가기'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFBBBBEE), // 배경색
                foregroundColor: Color(0xFF000000), // 텍스트색
                padding: EdgeInsets.symmetric(horizontal: 150, vertical: 15),
                textStyle: TextStyle(fontSize: fontSize * 0.8), 
              ),
            ),
          ],
        ),
      ),
    );
  }
}
