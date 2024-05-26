import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'package:matchup/models/UserProvider.dart';

final String baseUrl = 'http://172.30.1.72:8000/api/v1';

class RecordScreen extends StatefulWidget {
  @override
  _RecordScreenState createState() => _RecordScreenState();
}

class _RecordScreenState extends State<RecordScreen> {
  late Future<List<FlSpot>> pelvisSpots;
  late Future<List<FlSpot>> neckSpots;
  late Future<List<FlSpot>> legSpots;
  late Future<List<FlSpot>> waistSpots;
  late Future<List<HealthData>> healthDataListFuture;

  @override
  void initState() {
    super.initState();
    healthDataListFuture = fetchHealthData();
    pelvisSpots = fetchHealthSpots('pelvis');
    neckSpots = fetchHealthSpots('neck');
    legSpots = fetchHealthSpots('leg');
    waistSpots = fetchHealthSpots('waist');
  }

  Future<List<HealthData>> fetchHealthData() async {
    final userProvider = Provider.of<UserProvider>(context, listen: false);
    String? accessToken = userProvider.accessToken;

    if (accessToken == null) {
      throw Exception('Access token is null');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/health/graph/'),
      headers: <String, String>{
        'Authorization': 'Bearer $accessToken',
      },
    );

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((entry) => HealthData.fromJson(entry)).toList();
    } else {
      throw Exception('Failed to load health data');
    }
  }

  Future<List<FlSpot>> fetchHealthSpots(String metric) async {
    List<HealthData> healthDataList = await healthDataListFuture;
    return healthDataList.asMap().entries.map((entry) {
      int index = entry.key;
      HealthData data = entry.value;
      double x = index.toDouble(); // 날짜 대신 인덱스 사용
      double y = 0.0;
      switch (metric) {
        case 'waist':
          y = data.waist.toDouble();
          break;
        case 'leg':
          y = data.leg.toDouble();
          break;
        case 'pelvis':
          y = data.pelvis.toDouble();
          break;
        case 'neck':
          y = data.neck.toDouble();
          break;
      }
      return FlSpot(x, y);
    }).toList();
  }

  Widget buildSection(BuildContext context, String title, Future<List<FlSpot>> futureSpots) {
    var screenWidth = MediaQuery.of(context).size.width;
    var screenHeight = MediaQuery.of(context).size.height;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        ElevatedButton(
          onPressed: () {
            // Button action here
          },
          child: Text(title),
          style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18.0),
            ),
            backgroundColor: Color(0xFFBBBBEE),
            foregroundColor: Colors.black,
          ),
        ),
        SizedBox(height: screenHeight * 0.03),
        Container(
          height: screenHeight * 0.20,
          width: screenWidth * 0.90,
          alignment: Alignment.center,
          child: FutureBuilder<List<FlSpot>>(
            future: futureSpots,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return CircularProgressIndicator();
              } else if (snapshot.hasError) {
                return Text('Error: ${snapshot.error}');
              } else {
                return FutureBuilder<List<HealthData>>(
                  future: healthDataListFuture,
                  builder: (context, healthDataSnapshot) {
                    if (healthDataSnapshot.connectionState == ConnectionState.waiting) {
                      return CircularProgressIndicator();
                    } else if (healthDataSnapshot.hasError) {
                      return Text('Error: ${healthDataSnapshot.error}');
                    } else {
                      return PelvicTiltChart(
                        spots: snapshot.data!,
                        healthDataList: healthDataSnapshot.data!,
                      );
                    }
                  },
                );
              }
            },
          ),
        ),
        SizedBox(height: screenHeight * 0.03),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(MediaQuery.of(context).size.width * 0.04),
        child: ListView(
          children: <Widget>[
            buildSection(context, '골반', pelvisSpots),
            buildSection(context, '목', neckSpots),
            buildSection(context, '다리', legSpots),
            buildSection(context, '허리', waistSpots),
          ],
        ),
      ),
    );
  }
}

class PelvicTiltChart extends StatelessWidget {
  final List<FlSpot> spots;
  final List<HealthData> healthDataList;

  PelvicTiltChart({required this.spots, required this.healthDataList});

  @override
  Widget build(BuildContext context) {
    return LineChart(
      LineChartData(
        lineBarsData: [
          LineChartBarData(
            spots: spots,
            isCurved: true,
            gradient: LinearGradient(
              colors: [
                Colors.blueAccent,
                Colors.purpleAccent,
              ],
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
            ),
            barWidth: 5,
            isStrokeCapRound: true,
            dotData: FlDotData(show: true),
            belowBarData: BarAreaData(show: true),
          ),
        ],
        minY: 0,
        maxY: 100, // Adjust based on your data range
        minX: 0,
        maxX: (healthDataList.length - 1).toDouble(),
        titlesData: FlTitlesData(
          show: true,
          topTitles: AxisTitles(
            sideTitles: SideTitles(showTitles: false),
          ),
          rightTitles: AxisTitles(
            sideTitles: SideTitles(showTitles: false),
          ),
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 30,
              getTitlesWidget: (value, meta) {
                int index = value.toInt();
                if (index < 0 || index >= healthDataList.length) return Text('');
                return Text(healthDataList[index].formattedDate);
              },
              interval: 1,
            ),
          ),
        ),
        gridData: FlGridData(show: true),
        borderData: FlBorderData(show: false),
      ),
    );
  }
}

class HealthData {
  final int waist;
  final int leg;
  final int pelvis;
  final int neck;
  final int userId;
  final DateTime createdAt;

  HealthData({
    required this.waist,
    required this.leg,
    required this.pelvis,
    required this.neck,
    required this.userId,
    required this.createdAt,
  });

  factory HealthData.fromJson(Map<String, dynamic> json) {
    return HealthData(
      waist: json['waist'],
      leg: json['leg'],
      pelvis: json['pelvis'],
      neck: json['neck'],
      userId: json['user_id'],
      createdAt: DateTime.parse(json['createdAt']),
    );
  }

  String get formattedDate {
    return '${createdAt.month}/${createdAt.day}';
  }
}
