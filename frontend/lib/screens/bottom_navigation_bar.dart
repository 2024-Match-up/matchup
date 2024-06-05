import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'login/mypage_modal.dart';
import 'exercise/exercise_screen.dart';
import 'calendar/calendar_screen.dart';
import 'camera/camera_screen.dart';
import 'record/record_screen.dart';
import 'grade/grade_screen.dart';

class BottomNavBar extends StatefulWidget {
  final String accessToken;

  BottomNavBar({required this.accessToken});

  @override
  _BottomNavBarState createState() => _BottomNavBarState();
}

class _BottomNavBarState extends State<BottomNavBar> {
  int _selectedIndex = 0;

  // 각 탭의 위젯을 저장할 리스트를 생성합니다.
  final List<Widget> _widgetOptions = [
    ExerciseScreen(),  // 운동 페이지
    CalendarScreen(),  // 달력 페이지
    CameraScreen(),    // 카메라 페이지
    RecordScreen(),    // 측정기록 페이지
    GradeScreen() // 랭킹 페이지
  ];

  @override
  void initState() {
    super.initState();
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
      statusBarColor: Color(0xFFBBBBEE), // Top bar color
      statusBarIconBrightness: Brightness.light, // Status bar icons' color
    ));
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width; 

    return Scaffold(
      backgroundColor: Colors.grey[300], // Scaffold 배경색을 grey[300]으로 설정
      appBar: AppBar(
        backgroundColor: Color(0xFFBBBBEE), // AppBar 배경색 설정
        leading: Transform.translate(
          // 아이콘 이동
          offset: Offset(10.0, -3.0),
          child: IconButton(
            icon: Icon(Icons.account_circle),
            iconSize: screenWidth * 0.1, 
            onPressed: () {
              showMyPageModal(context, widget.accessToken); // 모달 창을 띄우는 함수 호출
            },
          ),
        ),
        centerTitle: true,
        elevation: 0,
        toolbarHeight: screenWidth * 0.15, // AppBar의 높이를 화면 너비의 비율로 설정
      ),
      body: Center(
        child: _widgetOptions.elementAt(_selectedIndex),
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          border: Border(
            top: BorderSide(color: Color(0xFF000000), width: 0.5),
          ),
        ),
        child: BottomNavigationBar(
          type: BottomNavigationBarType.fixed,
          showSelectedLabels: false,
          showUnselectedLabels: false,
          items: <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              icon: Icon(Icons.fitness_center, size: screenWidth * 0.07), 
              label: '운동',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.calendar_month, size: screenWidth * 0.07), 
              label: '달력',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.photo_camera, size: screenWidth * 0.07), 
              label: '카메라',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.timeline, size: screenWidth * 0.07),
              label: '그래프',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.emoji_events, size: screenWidth * 0.07),
              label: '랭킹',
            ),
          ],
          currentIndex: _selectedIndex,
          selectedItemColor: Color(0xFF000000),
          unselectedItemColor: Color(0xFF808080),
          onTap: _onItemTapped,
        ),
      ),
    );
  }
}