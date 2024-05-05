import 'package:flutter/material.dart';
import '/services/api_client.dart'; // API 클라이언트를 불러오는 경로를 확인하세요.

void showSignUpModal(BuildContext context) {
  var screenWidth = MediaQuery.of(context).size.width;
  var screenHeight = MediaQuery.of(context).size.height;

  // TextEditingController 인스턴스를 생성합니다.
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _nicknameController = TextEditingController();
  final TextEditingController _birthController = TextEditingController();
  final ApiClient _apiClient = ApiClient(); // API 클라이언트 인스턴스 생성

  showDialog(
    context: context,
    builder: (BuildContext context) {
      String _selectedGender = "Male"; // 성별 기본값
      return StatefulBuilder( // StatefulBuilder를 사용하여 내부 상태를 관리
        builder: (BuildContext context, StateSetter setState) {
          void _signup() async {
            try {
              DateTime birthDate;
              try {
                birthDate = DateTime.parse(_birthController.text); // 생일 문자열을 DateTime 객체로 변환
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("생일 형식이 잘못되었습니다.")));
                return;
              }

              await _apiClient.signup(
                _emailController.text,
                _passwordController.text,
                _nicknameController.text,
                birthDate,
                _selectedGender
              );
              Navigator.pop(context); // 성공 시 모달 닫기
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("회원가입 성공")));
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("회원가입 실패: $e")));
            }
          }

          return Dialog(
            backgroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20.0),
            ),
            child: Padding(
              padding: EdgeInsets.all(screenWidth * 0.05), 
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Text(
                    '회원가입',
                    style: TextStyle(
                      fontSize: screenWidth * 0.06, 
                      fontWeight: FontWeight.bold,
                      color: Colors.black
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: screenHeight * 0.03),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      IconButton(
                        icon: Icon(Icons.male),
                        iconSize: screenWidth * 0.08,
                        color: _selectedGender == 'Male' ? Colors.blue : Colors.grey,
                        onPressed: () {
                          setState(() {
                            _selectedGender = "Male";
                          });
                        },
                      ),
                      IconButton(
                        icon: Icon(Icons.female),
                        iconSize: screenWidth * 0.08,
                        color: _selectedGender == 'Female' ? Colors.pink : Colors.grey,
                        onPressed: () {
                          setState(() {
                            _selectedGender = "Female";
                          });
                        },
                      ),
                    ],
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextFormField(
                    controller: _birthController,
                    decoration: InputDecoration(
                      hintText: '생년월일 (YYYY-MM-DD)',
                      prefixIcon: Icon(Icons.cake),
                    ),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextFormField(
                    controller: _nicknameController,
                    decoration: InputDecoration(
                      hintText: '닉네임',
                      prefixIcon: Icon(Icons.person),
                    ),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextFormField(
                    controller: _emailController,
                    decoration: InputDecoration(
                      hintText: '이메일',
                      prefixIcon: Icon(Icons.mail),
                    ),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextFormField(
                    controller: _passwordController,
                    decoration: InputDecoration(
                      hintText: '비밀번호',
                      prefixIcon: Icon(Icons.lock),
                    ),
                    obscureText: true,
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  ElevatedButton(
                    onPressed: _signup,
                    child: Text('회원가입', style: TextStyle(fontSize: screenHeight * 0.02)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFFBBBBEE),
                      foregroundColor: Colors.black,
                      minimumSize: Size(screenWidth, screenHeight * 0.06),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.04),
                    ),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                ],
              ),
            ),
          );
        }
      );
    },
  );
}
