import 'package:flutter/material.dart';

void showSignUpModal(BuildContext context) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20.0), // 모서리를 둥글게 처리합니다.
        ),
        child: Container(
          padding: EdgeInsets.all(20),
          child: Wrap(
            // Column 대신 Wrap 위젯을 사용하여 내용이 화면을 벗어나지 않도록 합니다.
            children: <Widget>[
              Center(
                // '회원가입' 텍스트를 가운데 정렬합니다.
                child: Text(
                  '회원가입',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),
              SizedBox(height: 40), // 여기서 간격을 조절합니다.
              TextField(
                decoration: InputDecoration(
                  hintText: '닉네임',
                  contentPadding: EdgeInsets.fromLTRB(1, 8, 12, 0),
                  border: UnderlineInputBorder(),
                ),
                style: TextStyle(fontSize: 16),
              ),
              SizedBox(height: 50), // 닉네임 - 이메일 간격
              Row(
                mainAxisAlignment:
                    MainAxisAlignment.spaceBetween, // 버튼을 오른쪽으로 정렬합니다.
                children: [
                  Expanded(
                    child: TextField(
                      decoration: InputDecoration(
                        hintText: '이메일',
                        contentPadding: EdgeInsets.fromLTRB(1, 8, 12, 0),
                        border: UnderlineInputBorder(),
                      ),
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () {
                      // TODO: 이메일 중복 확인 로직 처리
                    },
                    child: Text('중복 확인'),
                    style: ElevatedButton.styleFrom(
                      padding:
                          EdgeInsets.symmetric(horizontal: 16), // 좌우 패딩을 줄입니다.
                      minimumSize:
                          Size(64, 32), // 버튼의 최소 크기를 설정합니다. 필요한 크기로 조절하세요.
                      textStyle: TextStyle(fontSize: 14), // 텍스트 스타일을 조절합니다.
                    ),
                  ),
                ],
              ),
              SizedBox(height: 30), // 이메일 - 비밀번호 간격
              TextField(
                decoration: InputDecoration(
                  hintText: '비밀번호',
                  contentPadding: EdgeInsets.fromLTRB(1, 8, 12, 0),
                  border: UnderlineInputBorder(),
                ),
                obscureText: true, // 비밀번호는 숨겨야 하므로 obscureText를 true로 설정합니다.
                style: TextStyle(fontSize: 16),
              ),
              SizedBox(height: 80), // 여기서 간격을 조절합니다.
              Center(
                // '회원가입' 버튼을 가운데 정렬합니다.
                child: ElevatedButton(
                  child: Text('회원가입'),
                  onPressed: () {
                    // 회원가입 로직 처리
                  },
                ),
              ),
              SizedBox(height: 50), // 마지막 버튼과 모달의 하단 간격을 조절합니다.
            ],
          ),
        ),
      );
    },
  );
}
