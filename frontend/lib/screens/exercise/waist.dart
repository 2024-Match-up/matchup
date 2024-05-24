import 'package:flutter/material.dart';
import 'exercise_camera.dart';

class WaistStretchScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double buttonHeight = screenWidth * 0.5;
    double fontSize = screenWidth * 0.04;
    double largeFontSize = screenWidth * 0.05;

    return Scaffold(
      appBar: AppBar(
        title: Text('허리 스트레칭'),
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
                      '방에서 쉽게 할 수 있는 맨몸 운동으로, 디스크나 인대, 관절로 전달되는 충격을 감소시킵니다. '
                      '따라서 척추의 통증을 예방하고 완화할 수 있습니다. ',
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
                      '1. 골반과 어깨를 수평으로 유지한다. \n'
                      '2. 손을 머리 뒤로 깍지를 끼고, 팔꿈치를 수평으로  \n'
                      '    유지한다. \n\n',
                      style: TextStyle(fontSize: fontSize),
                      textAlign: TextAlign.left,
                    ),
                    SizedBox(height: 0),
                    Center(
                      child: Text(
                        '횟수: 좌, 우로 10회씩 3세트',
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
                    MaterialPageRoute(builder: (context) => ExerciseCameraScreen(exerciseId: 4,)),
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
