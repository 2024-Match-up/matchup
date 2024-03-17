import 'package:flutter/material.dart';
import 'bottom_navigation_bar.dart';
import 'sign_up_modal.dart';

class LoginScreen extends StatelessWidget {
  // TextEditingController 인스턴스를 생성합니다.
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

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
            Image.asset('lib/assets/images/logo.jpg',
                height: 180, fit: BoxFit.contain),
            SizedBox(height: 0), // 로고와 입력 필드 사이의 여백을 늘립니다.
            Text(
              'Match up!',
              style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 48), // 텍스트와 입력 필드 사이의 여백을 늘립니다.

            // 이메일 입력 필드
            TextFormField(
              controller: _emailController,
              decoration: InputDecoration(
                hintText: '아이디',
                prefixIcon: Icon(Icons.person),
              ),
            ),
            SizedBox(height: 16),

            // 비밀번호 입력 필드
            TextFormField(
              controller: _passwordController,
              decoration: InputDecoration(
                hintText: '비밀번호',
                prefixIcon: Icon(Icons.lock),
              ),
              obscureText: true,
            ),
            SizedBox(height: 24),

            // 로그인 버튼
            OutlinedButton(
              child: Text('로그인'),
              onPressed: () {
                // TODO: 로그인 로직을 여기에 추가합니다.
                // 아래는 입력된 이메일과 비밀번호를 출력하는 예시입니다.
                print('이메일: ${_emailController.text}');
                print('비밀번호: ${_passwordController.text}');

                // 인증이 성공했다고 가정하고, 하단 탭 바 페이지로 이동합니다.
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => BottomNavBar()),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFBBBBEE), // 배경색
                foregroundColor: Color(0xFF000000), // 텍스트색
                side: BorderSide.none, // 테두리 제거
              ),
            ),
            SizedBox(height: 16),

            // 이메일 회원가입 버튼
            OutlinedButton(
              child: Text('이메일 회원가입'),
              onPressed: () {
                // 이메일 회원가입 로직 처리
                showSignUpModal(context);
              },
              style: OutlinedButton.styleFrom(
                backgroundColor: Color(0x14000000), // 배경색
                foregroundColor: Color(0xFF000000), // 텍스트색
                side: BorderSide.none, // 테두리 제거
              ),
            ),
            SizedBox(height: 16),

            // 이메일, 비밀번호 찾기
            TextButton(
              onPressed: () {
                // 이메일/비밀번호 찾기 로직 처리
              },
              child: Text(
                '이메일/비밀번호 찾기',
                style: TextStyle(
                  color: Colors.grey, // 텍스트 색상을 그레이로 설정합니다.
                  decoration: TextDecoration.underline, // 밑줄 추가
                ),
              ),
            ),

            // 카카오로 로그인 버튼(아이콘 이미지 포함되어있음)
            OutlinedButton.icon(
              icon: Image.asset('lib/assets/images/kakao_login.jpg',
                  height: 18.0),
              label: Text('카카오로 로그인'),
              onPressed: () {
                // 카카오 로그인 로직 처리
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFFFE600), // 카카오 컬러
                foregroundColor: Colors.black, // 텍스트 컬러
                side: BorderSide.none, // 테두리 제거
              ),
            ),
          ],
        ),
      ),
    );
  }
}
