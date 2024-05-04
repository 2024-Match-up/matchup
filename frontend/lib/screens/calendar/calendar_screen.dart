import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';

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
    _selectedDayExercises = _fetchExercisesForDay(_selectedDay);
  }

  List<String> _fetchExercisesForDay(DateTime day) {
    // Temporary hardcoded data for exercises
    // TODO: Replace with actual data fetching from backend when available
    return ['풀업', '딥스', '스쿼트']; // Example list of exercises
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Column(
        children: <Widget>[
          Card(
            margin: EdgeInsets.all(screenWidth * 0.02), // Responsive margin
            child: TableCalendar(
              headerStyle: HeaderStyle(
                formatButtonVisible: false, // This hides the format button
                titleCentered: true, // This will center the header title if desired
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
                  _selectedDayExercises = _fetchExercisesForDay(selectedDay);
                });
              },
            ),
          ),
          Expanded(
            child: Card(
              margin: EdgeInsets.all(screenWidth * 0.02), // Responsive margin
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
