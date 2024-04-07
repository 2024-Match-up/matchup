import 'package:flutter/material.dart';

void showSignUpModal(BuildContext context) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20.0),
        ),
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Text(
                '회원가입',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 20),
              buildTextField('닉네임'),
              SizedBox(height: 20),
              buildTextField('이메일'),
              SizedBox(height: 20),
              buildTextField('비밀번호', isPassword: true),
              SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () {
                        // 회원가입 로직 처리
                      },
                      child: Text('회원가입'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFFBBBBEE), 
                        foregroundColor: Colors.white, 
                        minimumSize: Size(0, 36), // 높이 설정, 너비는 Expanded로 조절
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.symmetric(horizontal: 16),
                      ),
                    ),
                  ),
                  SizedBox(width: 8), // 버튼 사이의 간격
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () {
                        // 이메일 중복 확인 로직 처리
                      },
                      child: Text('중복 확인'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFFBBBBEE), 
                        foregroundColor: Colors.white, 
                        minimumSize: Size(0, 36), // 높이 설정, 너비는 Expanded로 조절
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.symmetric(horizontal: 16),
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16),
            ],
          ),
        ),
      );
    },
  );
}

Widget buildTextField(String hintText, {bool isPassword = false}) {
  return Container(
    height: 50, // 텍스트 필드 높이 설정
    child: TextField(
      obscureText: isPassword, // 비밀번호 필드 여부 설정
      textAlignVertical: TextAlignVertical.center,
      decoration: InputDecoration(
        hintText: hintText,
        contentPadding: EdgeInsets.symmetric(horizontal: 10.0),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10.0),
        ),
      ),
    ),
  );
}

class IconLabel extends StatelessWidget {
  final IconData icon;
  final String label;

  const IconLabel({
    Key? key,
    required this.icon,
    required this.label,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Icon(icon, size: 48),
        SizedBox(height: 8), // 아이콘과 텍스트 사이의 간격 설정
        Text(label),
      ],
    );
  }
}
