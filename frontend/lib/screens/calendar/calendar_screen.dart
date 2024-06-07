import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:provider/provider.dart';
import 'package:matchup/models/UserProvider.dart';
import 'package:http/http.dart' as http;

class CalendarScreen extends StatefulWidget {
  @override
  _CalendarScreenState createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  late DateTime _focusedDay;
  late DateTime _selectedDay;
  List<String> _selectedDayExercises = [];

  @override
  void initState() {
    super.initState();
    _focusedDay = DateTime.now();
    _selectedDay = DateTime.now();
    _fetchExercisesForDay(_selectedDay);
  }

  Future<void> _fetchExercisesForDay(DateTime day) async {
    final userProvider = Provider.of<UserProvider>(context, listen: false);
    String? accessToken = userProvider.accessToken;
    final String baseUrl = 'http://172.30.1.72:8000/api/v1';


    final response = await http.get(
      Uri.parse('$baseUrl/session?date=${day.toIso8601String().split('T')[0]}'),
      headers: {
        'Authorization': 'Bearer $accessToken',
        'Content-Type': 'application/json; charset=utf-8',
      },
    );

    if (response.statusCode == 200) {
      List<dynamic> exercises = json.decode(utf8.decode(response.bodyBytes));
      setState(() {
        _selectedDayExercises = exercises
            .where((exercise) => DateTime.parse(exercise['date']).toLocal().toIso8601String().split('T')[0] == day.toIso8601String().split('T')[0])
            .map((exercise) => exercise['exercise'].toString())
            .toList();
      });
    } else {
      setState(() {
        _selectedDayExercises = [];
      });
      throw Exception('Failed to load exercises');
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Column(
        children: <Widget>[
          Card(
            margin: EdgeInsets.all(screenWidth * 0.02),
            child: TableCalendar(
              headerStyle: HeaderStyle(
                formatButtonVisible: false,
                titleCentered: true,
              ),
              locale: 'ko_KR',
              focusedDay: _focusedDay,
              firstDay: DateTime.utc(2010, 10, 16),
              lastDay: DateTime.utc(2030, 3, 14),
              selectedDayPredicate: (day) {
                return isSameDay(_selectedDay, day);
              },
              onDaySelected: (selectedDay, focusedDay) {
                setState(() {
                  _selectedDay = selectedDay;
                  _focusedDay = focusedDay;
                });
                _fetchExercisesForDay(selectedDay);
              },
            ),
          ),
          Expanded(
            child: Card(
              margin: EdgeInsets.all(screenWidth * 0.02),
              child: ListView.builder(
                itemCount: _selectedDayExercises.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(_selectedDayExercises[index]),
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}
