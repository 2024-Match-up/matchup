import 'package:flutter/material.dart';
import '../bottom_navigation_bar.dart';
import 'sign_up_modal.dart';
import '/services/api_client.dart';
import 'package:matchup/models/UserProvider.dart';
import 'package:provider/provider.dart';


class LoginScreen extends StatelessWidget {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  final ApiClient _apiClient = ApiClient();

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(screenWidth * 0.04), // Responsive padding
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              // 로고 이미지
              SizedBox(height: screenHeight * 0.1),
              Image.asset('lib/assets/images/logo.jpg', height: screenHeight * 0.2, fit: BoxFit.contain),
              SizedBox(height: screenHeight * 0.03),

              Text(
                'Match up!',
                style: TextStyle(fontSize: screenWidth * 0.1, fontFamily: "Timmana", fontWeight: FontWeight.w300),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: screenHeight * 0.05),

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
                onPressed: () async {
                  try {
                    // 로그인 메서드 호출하고 토큰을 받음
                    String accessToken = await _apiClient.login(
                      _emailController.text,
                      _passwordController.text,
                    );
                    
                    // 로그로 액세스 토큰 출력
                    print('로그인 성공! 액세스 토큰: $accessToken');
                    Provider.of<UserProvider>(context, listen: false).login(accessToken);
                    
                    // 인증 성공 후 하단 탭 바 페이지로 이동하고 토큰을 전달
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => BottomNavBar(accessToken: accessToken),
                      ),
                    );
                  } catch (e) {
                    // 에러 처리
                    ScaffoldMessenger.of(context)
                        .showSnackBar(SnackBar(content: Text('Login failed: $e')));
                    print('로그인 실패: $e');
                  }
                },
                style: OutlinedButton.styleFrom(
                  backgroundColor: Color(0xFFBBBBEE),
                  foregroundColor: Color(0xFF000000),
                  side: BorderSide.none,
                ).copyWith(
                  minimumSize: MaterialStatePropertyAll(Size(screenWidth * 0.8, screenHeight * 0.08)),
                ),
              ),
              SizedBox(height: screenHeight * 0.025),
              // 이메일 회원가입 버튼
              OutlinedButton(
                child: Text(
                  '이메일 회원가입',
                  style: TextStyle(fontSize: screenHeight * 0.02),
                ),
                onPressed: () {
                  // 회원가입 모달 표시
                  showSignUpModal(context);
                },
                style: OutlinedButton.styleFrom(
                  backgroundColor: Color(0x14000000),
                  foregroundColor: Color(0xFF000000),
                  side: BorderSide.none,
                ).copyWith(
                  minimumSize: MaterialStatePropertyAll(Size(screenWidth * 0.8, screenHeight * 0.08)),
                ),
              ),
              SizedBox(height: screenHeight * 0.025),
            ],
          ),
        ),
      ),
    );
  }
}