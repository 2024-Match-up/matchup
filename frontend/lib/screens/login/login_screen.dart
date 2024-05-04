import 'package:flutter/material.dart';
import '../bottom_navigation_bar.dart'; 
import 'sign_up_modal.dart'; 

class LoginScreen extends StatelessWidget {
  // TextEditingController 인스턴스를 생성합니다.
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(screenWidth * 0.04), // Responsive padding
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            // 로고 이미지
            Image.asset('lib/assets/images/logo.jpg', height: screenHeight * 0.2, fit: BoxFit.contain),
            SizedBox(height: screenHeight * 0.03), // 로고와 입력 필드 사이의 여백을 늘립니다.

            Text(
              'Match up!',
              style: TextStyle(fontSize: screenWidth * 0.1, fontFamily: "Timmana", fontWeight: FontWeight.w300),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: screenHeight * 0.05), // 텍스트와 입력 필드 사이의 여백을 늘립니다.

            // 이메일 입력 필드
            TextFormField(
              controller: _emailController,
              decoration: InputDecoration(
                hintText: '아이디',
                prefixIcon: Icon(Icons.person),
              ),
            ),
            SizedBox(height: screenHeight * 0.025),

            // 비밀번호 입력 필드
            TextFormField(
              controller: _passwordController,
              decoration: InputDecoration(
                hintText: '비밀번호',
                prefixIcon: Icon(Icons.lock),
              ),
              obscureText: true,
            ),
            SizedBox(height: screenHeight * 0.03),

            // 로그인 버튼
            OutlinedButton(
              child: Text(
                '로그인',
                style: TextStyle(fontSize: screenHeight * 0.02),
              ),
              onPressed: () {
                // 로그인 로직을 여기에 추가합니다.
                print('이메일: ${_emailController.text}');
                print('비밀번호: ${_passwordController.text}');

                // 인증이 성공했다고 가정하고, 하단 탭 바 페이지로 이동합니다.
                Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => BottomNavBar()));
              },
              style: OutlinedButton.styleFrom(
                backgroundColor: Color(0xFFBBBBEE), // 배경색
                foregroundColor: Color(0xFF000000), // 텍스트색
                side: BorderSide.none, // 테두리 제거
              ).copyWith(minimumSize: MaterialStatePropertyAll(Size(screenWidth * 0.5, 65)))
            ),
            SizedBox(height: screenHeight * 0.025),

            // 이메일 회원가입 버튼
            OutlinedButton(
              child: Text(
                '이메일 회원가입',
                style: TextStyle(fontSize: screenHeight * 0.02),
              ),
              onPressed: () {
                // 이메일 회원가입 로직 처리
                showSignUpModal(context);
              },
              style: OutlinedButton.styleFrom(
                backgroundColor: Color(0x14000000), // 배경색
                foregroundColor: Color(0xFF000000), // 텍스트색
                side: BorderSide.none, // 테두리 제거
              ).copyWith(minimumSize: MaterialStatePropertyAll(Size(screenWidth * 0.5, 65)))
            ),
            SizedBox(height: screenHeight * 0.025),
          ],
        ),
      ),
    );
  }
}

