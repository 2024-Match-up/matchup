import 'package:flutter/material.dart';

void showMyPageModal(BuildContext context) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20.0),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Text(
                '내 프로필',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 22,
                ),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  GestureDetector(
                    // onTap: () => 
                    child: IconLabel(icon: Icons.male, label: '남'),
                  ),
                  GestureDetector(
                    child: IconLabel(icon: Icons.female, label: '여'),
                  ),
                ],
              ),
              SizedBox(height: 20),
              Container(
                height: 50, // 텍스트 필드 높이 설정
                child:TextField(
                  textAlignVertical: TextAlignVertical.center,
                  decoration: InputDecoration(
                    hintText: '이름',
                    contentPadding: EdgeInsets.symmetric(horizontal: 10.0),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                      ),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Container(
                height: 50, // 텍스트 필드 높이 설정
                child:TextField(
                  textAlignVertical: TextAlignVertical.center,
                  decoration: InputDecoration(
                    hintText: '생일',
                    contentPadding: EdgeInsets.symmetric(horizontal: 10.0),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                      ),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Container(
                height: 50, // 텍스트 필드 높이 설정
                child:TextField(
                  textAlignVertical: TextAlignVertical.center,
                  decoration: InputDecoration(
                    hintText: '신장',
                    contentPadding: EdgeInsets.symmetric(horizontal: 10.0),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                      ),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Container(
                height: 50, // 텍스트 필드 높이 설정
                child:TextField(
                  textAlignVertical: TextAlignVertical.center,
                  decoration: InputDecoration(
                    hintText: '몸무게',
                    contentPadding: EdgeInsets.symmetric(horizontal: 10.0),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                      ),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  Expanded( // Expanded 위젯으로 감싸서 버튼을 가로로 길게 합니다.
                    child: TextButton(
                      child: Text('확인'),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.black, // Text Color
                        backgroundColor: Color(0xFFBBBBEE), // Button Background Color
                        minimumSize: Size(double.infinity, 36), // 높이를 36으로 설정하고 너비를 무한대로 설정하여 가로로 길게 합니다.
                        padding: EdgeInsets.symmetric(horizontal: 16), // 좌우 패딩 추가
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
        Text(label),
      ],
    );
  }
}