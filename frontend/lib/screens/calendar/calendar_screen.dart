// import 'package:flutter/material.dart';
// import 'package:table_calendar/table_calendar.dart';
// import 'package:http/http.dart' as http;
// import 'dart:convert';

// class CalendarScreen extends StatefulWidget {
//   @override
//   _CalendarScreenState createState() => _CalendarScreenState();
// }

// class _CalendarScreenState extends State<CalendarScreen> {
//   late DateTime _focusedDay;
//   late DateTime _selectedDay;
//   List<String> _selectedDayExercises = [];
//   bool _isLoading = false;

//   @override
//   void initState() {
//     super.initState();
//     _focusedDay = DateTime.now();
//     _selectedDay = DateTime.now();
//     _fetchExercisesForDay(_selectedDay);
//   }

//   Future<void> _fetchExercisesForDay(DateTime day) async {
//     setState(() {
//       _isLoading = true; // Show a loading indicator
//     });
    
//     // Simulate a network request delay
//     await Future.delayed(Duration(seconds: 1));

//     // The URL for your API goes here
//     var url = Uri.parse('https://your-api.com/exercises?date=${day.toIso8601String()}');
    
//     try {
//       var response = await http.get(url);

//       if (response.statusCode == 200) {
//         var data = json.decode(response.body);
//         // Assuming the response body is a list of exercise names
//         List<String> exercises = List<String>.from(data['exercises']);

//         setState(() {
//           _selectedDayExercises = exercises;
//         });
//       } else {
//         // If the server did not return a 200 OK response,
//         // then throw an exception.
//         throw Exception('Failed to load exercises');
//       }
//     } catch (e) {
//       // Handle any errors here
//       print(e);
//     }

//     setState(() {
//       _isLoading = false; // Hide the loading indicator
//     });
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: Column(
//         children: <Widget>[
//           Card(
//             margin: const EdgeInsets.all(8.0),
//             child: TableCalendar(
//               headerStyle: HeaderStyle(
//                 formatButtonVisible: false, // This hides the format button
//                 titleCentered: true, // This will center the header title if desired
//               ),
//               locale: 'ko_KR',
//               focusedDay: _focusedDay,
//               firstDay: DateTime.utc(2010, 10, 16),
//               lastDay: DateTime.utc(2030, 3, 14),
//               selectedDayPredicate: (day) {
//                 // Use `selectedDayPredicate` to determine which day is currently selected.
//                 // If this returns true, then `day` will be marked as selected.
//                 return isSameDay(_selectedDay, day);
//               },
//               onDaySelected: (selectedDay, focusedDay) {
//                 if (!isSameDay(_selectedDay, selectedDay)) {
//                   setState(() {
//                     _selectedDay = selectedDay;
//                     _focusedDay = focusedDay;
//                   });
//                   _fetchExercisesForDay(selectedDay);
//                 }
//               },
//             ),
//           ),
//           Expanded(
//             child: _isLoading
//                 ? Center(child: CircularProgressIndicator())
//                 : Card(
//                     margin: const EdgeInsets.all(8.0),
//                     child: ListView.builder(
//                       itemCount: _selectedDayExercises.length,
//                       itemBuilder: (context, index) {
//                         return ListTile(
//                           title: Text(_selectedDayExercises[index]),
//                         );
//                       },
//                     ),
//                   ),
//           ),
//         ],
//       ),
//     );
//   }
// }


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
    return Scaffold(
      body: Column(
        children: <Widget>[
          Card(
            margin: const EdgeInsets.all(8.0),
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
                // Use `selectedDayPredicate` to determine which day is currently selected.
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
              margin: const EdgeInsets.all(8.0),
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