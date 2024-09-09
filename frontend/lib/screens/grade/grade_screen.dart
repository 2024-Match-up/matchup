import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'dart:convert';
import 'package:matchup/models/UserProvider.dart';
import 'package:intl/intl.dart';

class GradeScreen extends StatefulWidget {
  @override
  _GradeScreenState createState() => _GradeScreenState();
}

class _GradeScreenState extends State<GradeScreen> {
  final String baseUrl = 'http://localhost:8000/api/v1';
  // final String baseUrl = 'http://10.254.3.138:8000/api/v1';

  Future<Map<int, List<SessionScore>>> fetchScores(String token) async {
    Map<int, List<SessionScore>> exerciseScores = {
      3: [],
      4: []
    }; // 기본적으로 빈 리스트 할당
    var response = await http.get(Uri.parse('$baseUrl/exercise/scores'),
        headers: {'Authorization': 'Bearer $token'});
    if (response.statusCode == 200) {
      List<dynamic> allScoresJson = jsonDecode(response.body);
      for (var scoreJson in allScoresJson) {
        SessionScore score = SessionScore.fromJson(scoreJson);
        if (score.exerciseId == 3 || score.exerciseId == 4) {
          exerciseScores[score.exerciseId]!.add(score);
        }
      }
    } else {
      throw Exception('Failed to load scores');
    }
    return exerciseScores;
  }

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context, listen: false);
    final token = userProvider.accessToken;

    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return DefaultTabController(
      length: 2, // 스쿼트와 런지, 두 가지 탭
      child: Scaffold(
        body: FutureBuilder(
          future: fetchScores(token!),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              if (snapshot.hasError) {
                return Text("Error: ${snapshot.error}");
              } else {
                var exerciseScores =
                    snapshot.data as Map<int, List<SessionScore>>?;
                return Column(
                  children: <Widget>[
                    TabBar(
                      labelColor: Colors.black,
                      labelStyle: TextStyle(fontSize: screenWidth * 0.04),
                      tabs: [
                        Tab(text: '스쿼트'), // ID 3
                        Tab(text: '런지'), // ID 4
                      ],
                    ),
                    Expanded(
                      child: TabBarView(
                        children: [
                          buildRankingList(exerciseScores?[3] ?? [],
                              screenWidth, screenHeight), // 스쿼트 탭 뷰
                          buildRankingList(exerciseScores?[4] ?? [],
                              screenWidth, screenHeight), // 런지 탭 뷰
                        ],
                      ),
                    ),
                  ],
                );
              }
            } else {
              return Center(child: CircularProgressIndicator());
            }
          },
        ),
      ),
    );
  }

  Widget buildRankingList(
      List<SessionScore> scores, double screenWidth, double screenHeight) {
    // 점수를 내림차순으로 정렬
    scores.sort((a, b) => b.score.compareTo(a.score));

    return ListView.builder(
      itemCount: scores.isEmpty ? 1 : scores.length,
      itemBuilder: (context, index) {
        if (scores.isEmpty) {
          return ListTile(
            title: Text('No data available',
                style: TextStyle(fontSize: screenWidth * 0.045)),
            subtitle:
                Text('점수: 0', style: TextStyle(fontSize: screenWidth * 0.035)),
          );
        }
        return ListTile(
          leading: _leadingIcon(index, screenWidth),
          title: Text(scores[index].getFormattedDate(),
              style: TextStyle(fontSize: screenWidth * 0.045)), // 포맷된 날짜 사용
          subtitle: Text('점수: ${scores[index].score}',
              style: TextStyle(fontSize: screenWidth * 0.035)),
        );
      },
    );
  }

  Widget _leadingIcon(int index, double screenWidth) {
    // 순위에 따라 다른 아이콘 표시
    int rank = index + 1; // 0-based index를 1-based 순위로 변환
    switch (rank) {
      case 1:
        return Icon(Icons.emoji_events, color: Color(0xFFFFD700)); // Gold
      case 2:
        return Icon(Icons.emoji_events, color: Color(0xFFC0C0C0)); // Silver
      case 3:
        return Icon(Icons.emoji_events, color: Color(0xFFCD7F32)); // Bronze
      default:
        return Text('$rank',
            style: TextStyle(fontSize: screenWidth * 0.035)); // 그 외 순위
    }
  }
}

class SessionScore {
  final String date;
  final int score;
  final int exerciseId;

  SessionScore(
      {required this.date, required this.score, required this.exerciseId});

  factory SessionScore.fromJson(Map<String, dynamic> json) {
    return SessionScore(
        date: json['date'],
        score: json['score'],
        exerciseId: json['exercise_id']);
  }

  String getFormattedDate() {
    // ISO8601 문자열을 DateTime 객체로 파싱
    DateTime parsedDate = DateTime.parse(date);
    // 원하는 형식으로 날짜 포맷
    return DateFormat('yyyy-MM-dd HH:mm').format(parsedDate);
  }
}
