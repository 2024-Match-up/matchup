import 'package:flutter/material.dart';
import 'exercise_camera.dart';

class HipStretchScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double buttonHeight = screenWidth * 0.5;
    double fontSize = screenWidth * 0.04;
    double largeFontSize = screenWidth * 0.05;

    return Scaffold(
      appBar: AppBar(
        title: Text('골반 스트레칭'),
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
                      '방에서 쉽게 할 수 있는 맨몸 스트레칭으로, 대퇴사두근, 햄스트링, 종아리 근육을 포함한 다리 근육을 만드는데 도움이 됩니다. '
                      '또한 몸 전체 근육을 촉진하는 효과적인 운동입니다. ',
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
                      '1. 뒷꿈치가 충분히 바닥에 닿을 수 있는 넓이로 \n'
                      '    발을 벌린다.\n'
                      '2. 무리하지 않고 앉을 수 있는 수준으로 쪼그려 앉는다. \n'
                      '3. 3초를 버틴 후 다시 일어난다.\n\n',
                      style: TextStyle(fontSize: fontSize),
                      textAlign: TextAlign.left,
                    ),
                    SizedBox(height: 0),
                    Center(
                      child: Text(
                        '횟수: 10회씩 3세트',
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
