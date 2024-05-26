import 'package:flutter/material.dart';
import 'neck.dart'; 
import 'hip.dart';
import 'waist.dart';
import 'leg.dart';

class ExerciseScreen extends StatefulWidget {
  @override
  _ExerciseScreenState createState() => _ExerciseScreenState();
}

class _ExerciseScreenState extends State<ExerciseScreen> {

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
          onTap: () {
            _navigateToScreen(NeckStretchScreen());
          },
        ),
        ExerciseCard(
          title: '골반 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          onTap: () {
            _navigateToScreen(HipStretchScreen());
          },
        ),
        ExerciseCard(
          title: '다리 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          onTap: () {
            _navigateToScreen(LegStretchScreen());
          },
        ),
        ExerciseCard(
          title: '허리 스트레칭',
          duration: '15min',
          calories: '-500kcal',
          sets: '4 sets',
          reps: '8-10 reps',
          onTap: () {
            _navigateToScreen(WaistStretchScreen());
          },
        ),
      ],
    );
  }

  void _navigateToScreen(Widget screen) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => screen),
    );
  }
}

class ExerciseCard extends StatelessWidget {
  final String title;
  final String duration;
  final String calories;
  final String sets;
  final String reps;
  final VoidCallback? onTap;

  const ExerciseCard({
    Key? key,
    required this.title,
    required this.duration,
    required this.calories,
    required this.sets,
    required this.reps,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var screenWidth = MediaQuery.of(context).size.width;

    return GestureDetector(
      onTap: onTap,
      child: Card(
        margin: EdgeInsets.all(screenWidth * 0.015),
        child: Padding(
          padding: EdgeInsets.all(screenWidth * 0.03),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
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
      ),
    );
  }
}
