import 'package:flutter/material.dart';

void showMyPageModal(BuildContext context) {
  var screenWidth = MediaQuery.of(context).size.width;
  var screenHeight = MediaQuery.of(context).size.height;

  showDialog(
    context: context,
    builder: (BuildContext context) {
      return Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(screenWidth * 0.05),
        ),
        child: Padding(
          padding: EdgeInsets.all(screenWidth * 0.05),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Text(
                '내 프로필',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: screenHeight * 0.03,
                ),
              ),
              SizedBox(height: screenHeight * 0.02),
              for (String field in ['닉네임','신장', '몸무게']) ...[
                Container(
                  height: screenHeight * 0.07, // 텍스트 필드 높이 동적 설정
                  margin: EdgeInsets.only(bottom: screenHeight * 0.02),
                  child: TextField(
                    textAlignVertical: TextAlignVertical.center,
                    decoration: InputDecoration(
                      hintText: field,
                      contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.02),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                    ),
                  ),
                ),
              ],
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  Expanded( // Expanded 위젯으로 감싸서 버튼을 가로로 길게 합니다.
                    child: TextButton(
                      child: Text('확인', style: TextStyle(fontSize: screenWidth * 0.04)),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.black, // Text Color
                        backgroundColor: Color(0xFFBBBBEE), // Button Background Color
                        minimumSize: Size(double.infinity, screenHeight * 0.06), // 높이 동적 설정
                        padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.03), // 좌우 패딩 추가
                      ),
                      onPressed: () {
                        Navigator.of(context).pop(); // 모달을 닫습니다.
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      );
    },
  );
}
