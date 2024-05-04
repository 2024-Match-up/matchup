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
        ),
        ExerciseCard(
          title: '골반 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
        ),
        ExerciseCard(
          title: '다리 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
        ),
        ExerciseCard(
          title: '허리 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
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

  const ExerciseCard({
    Key? key,
    required this.title,
    required this.duration,
    required this.calories,
    required this.sets,
    required this.reps,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var screenWidth = MediaQuery.of(context).size.width;

    return Card(
      margin: EdgeInsets.all(screenWidth * 0.015), 
      child: Padding(
        padding: EdgeInsets.all(screenWidth * 0.03), 
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            SizedBox(width: screenWidth * 0.01), 
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: screenWidth * 0.035, 
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: screenWidth * 0.03), 
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      Text(duration),
                      Text(sets),
                    ],
                  ),
                  SizedBox(height: screenWidth * 0.03), 
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
