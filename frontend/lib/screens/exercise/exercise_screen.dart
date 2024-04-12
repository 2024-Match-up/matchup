import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class ExerciseScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: <Widget>[
        ExerciseCard(
          title: '목 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          icon: FontAwesomeIcons.personWalking,
        ),
        ExerciseCard(
          title: '골반 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          icon: Icons.directions_run,
        ),
        ExerciseCard(
          title: '다리 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          icon: Icons.directions_run,
        ),
        ExerciseCard(
          title: '허리 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          icon: Icons.directions_run,
        ),
      ],
    );
  }
}

class ExerciseCard extends StatelessWidget {
  final String title;
  final String duration;
  final String calories;
  final String sets;
  final String reps;
  final IconData icon;

  const ExerciseCard({
    Key? key,
    required this.title,
    required this.duration,
    required this.calories,
    required this.sets,
    required this.reps,
    required this.icon,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.all(8.0),
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center, 
          children: <Widget>[
            Icon(icon, size: 50), // Display the icon
            SizedBox(width: 24), // Add space between the icon and the text
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      Text(duration),
                      Text(sets),
                    ],
                  ),
                  SizedBox(height: 4),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      Text(calories),
                      Text(reps),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}