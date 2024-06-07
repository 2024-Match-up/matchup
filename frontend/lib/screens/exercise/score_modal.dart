import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../bottom_navigation_bar.dart';  
import '../../models/UserProvider.dart';  

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
              // UserProvider로부터 accessToken 가져오기
              final userProvider = Provider.of<UserProvider>(context, listen: false);
              final String? accessToken = userProvider.accessToken;
              // BottomNavBar로 이동
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (context) => BottomNavBar(accessToken: accessToken ?? '')),
                (Route<dynamic> route) => false,
              );
            },
            child: Text('종료'),
          ),
        ),
      ],
    );
  }
}
