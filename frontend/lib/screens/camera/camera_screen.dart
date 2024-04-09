import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'body_scan.dart';

class CameraScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            // 로고 이미지
            Image.asset('lib/assets/images/logo.jpg', height: 180, fit: BoxFit.contain),
            Text(
              'Match up!',
              style: TextStyle(fontSize: 60, fontFamily: "Timmana", fontWeight: FontWeight.w300),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 60), // 텍스트와 입력 필드 사이의 여백을 늘립니다.
            ElevatedButton(
              child: Text('체형 측정하기'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFBBBBEE), // 배경색
                foregroundColor: Color(0xFF000000), 
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                textStyle: TextStyle(fontSize: 17),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => BodyScanScreen()),
                      );
              },
            ),
          ],
        ),
      ),
    );
  }
}
