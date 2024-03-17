import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'select_screen.dart'; // 운동 페이지
import 'calendar_screen.dart'; // 달력 페이지
import 'share_screen.dart'; // 친구 추가 페이지
import 'game_screen.dart'; // 게임 페이지

class BottomNavBar extends StatefulWidget {
  @override
  _BottomNavBarState createState() => _BottomNavBarState();
}

class _BottomNavBarState extends State<BottomNavBar> {
  int _selectedIndex = 0;

  // 각 탭의 위젯을 저장할 리스트를 생성합니다.
  final List<Widget> _widgetOptions = [
    // HomeScreen(),  // 홈 탭에 해당하는 위젯
    // ScheduleScreen(),  // 일정 탭에 해당하는 위젯
    // AddScreen(),  // 추가 탭에 해당하는 위젯
    // SettingsScreen(),  // 설정 탭에 해당하는 위젯
    Text('Home Screen'), // 임시 위젯
    Text('Schedule Screen'),
    Text('Add Screen'),
    Text('Settings Screen'),
  ];

  @override
  void initState() {
    super.initState();
    // Set status bar color
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
    return Scaffold(
      backgroundColor: Colors.grey[300], // Scaffold 배경색을 grey[300]으로 설정
      appBar: AppBar(
        backgroundColor: Color(0xFFBBBBEE), // AppBar 배경색 설정
        leading: Transform.translate(
          // 아이콘 이동
          offset: Offset(10.0, -3.0),
          child: IconButton(
            icon: Icon(Icons.account_circle),
            iconSize: 55.0, // 아이콘 크기
            onPressed: () {
              // 아이콘 버튼을 눌렀을 때 수행할 동작
            },
          ),
        ),
        centerTitle: true,
        elevation: 0,
        // AppBar의 높이를 70.0으로
        toolbarHeight: 70.0,
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
              icon: Icon(Icons.fitness_center, size: 30),
              label: '운동',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.calendar_today, size: 30),
              label: '달력',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person_add, size: 30),
              label: '친구 추가',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.videogame_asset, size: 30),
              label: '게임',
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

void main() {
  runApp(MaterialApp(
    title: 'match up!',
    theme: ThemeData(
      primaryColor: Color(0xFFBBBBEE),
      scaffoldBackgroundColor:
          Colors.grey[300], // Grey color for the main background
    ),
    home: BottomNavBar(),
  ));
}
