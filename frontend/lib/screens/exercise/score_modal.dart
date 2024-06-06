import 'package:flutter/material.dart';

class ScoreModal extends StatelessWidget {
  final double score;
  final String exerciseName;

  ScoreModal({required this.score, required this.exerciseName});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      title: Center(child: Text(exerciseName)),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.fitness_center, size: 40),
              SizedBox(width: 10),
              Text(
                '$score점',
                style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          SizedBox(height: 20),
          Text(
            '고생하셨습니다!',
            style: TextStyle(fontSize: 20),
          ),
        ],
      ),
      actions: [
        Center(
          child: ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: Text('종료'),
          ),
        ),
      ],
    );
  }
}
