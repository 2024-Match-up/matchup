import 'package:flutter/material.dart';
import 'exercise_camera.dart';

class NeckStretchScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double buttonHeight = screenWidth * 0.5;
    double fontSize = screenWidth * 0.04;
    double largeFontSize = screenWidth * 0.05;

    return Scaffold(
      appBar: AppBar(
        title: Text('목 스트레칭'),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              SizedBox(height: 25),
              Container(
                margin: EdgeInsets.all(20),
                padding: EdgeInsets.all(20),
                width: double.infinity,
                color: Colors.grey[200],
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Text(
                        '운동 설명',
                        style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    SizedBox(height: 30),
                    Text(
                      '목 체형 교정에 도움이 되는 운동입니다. '
                      '목은 머리 무게를 담당하는 중요한 부위입니다. '
                      '거북목을 치료하고 경추의 올바른 모양을 바로잡고 두통, 어깨 뭉침 증상을 완화합니다.',
                      style: TextStyle(fontSize: fontSize),
                      textAlign: TextAlign.left,
                    ),
                    SizedBox(height: 30),
                  ],
                ),
              ),
              SizedBox(height: 30),
              Container(
                margin: EdgeInsets.all(20),
                padding: EdgeInsets.all(20),
                width: double.infinity,
                color: Colors.grey[200],
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Text(
                        '운동 방법',
                        style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    SizedBox(height: 30),
                    Text(
                      '1. 벽에 어깨와 엉덩이, 발목을 붙인다.\n'
                      '2. 다리, 골반, 어깨 순으로 벽에서 떨어트려 비스듬히 \n'
                      '    선다.\n'
                      '3. 목으로 체중을 지탱하며 일정한 각도를 유지한다.\n'
                      '4. 5초씩 버틴 후 다시 벽에 기댄다.\n\n',
                      style: TextStyle(fontSize: fontSize),
                      textAlign: TextAlign.left,
                    ),
                    SizedBox(height: 0),
                    Center(
                      child: Text(
                        '횟수: 3회씩 3세트',
                        style: TextStyle(fontSize: largeFontSize, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 30),
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
      ),
    );
  }
}
