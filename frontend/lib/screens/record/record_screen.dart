import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class RecordScreen extends StatelessWidget {
  Widget buildSection(BuildContext context, String title) {
    var screenWidth = MediaQuery.of(context).size.width;
    var screenHeight = MediaQuery.of(context).size.height;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        ElevatedButton(
          onPressed: () {
            // 버튼 동작을 여기에 정의합니다.
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
        SizedBox(height: screenHeight * 0.03), // Responsive spacing
        Container(
          height: screenHeight * 0.20, // 20% of total screen height
          width: screenWidth * 0.90, // 90% of total screen width
          alignment: Alignment.center,
          child: PelvicTiltChart(),
        ),
        SizedBox(height: screenHeight * 0.03), // Responsive spacing
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
            buildSection(context, '골반'),
            buildSection(context, '목'),
            buildSection(context, '다리'),
            buildSection(context, '허리'),
          ],
        ),
      ),
    );
  }
}

class PelvicTiltChart extends StatelessWidget {
  final List<FlSpot> spots = [
    FlSpot(0, 1),
    FlSpot(1, 3),
    FlSpot(2, 5),
    FlSpot(3, 7),
    FlSpot(4, 9),
  ];

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
        maxY: 10,
        titlesData: FlTitlesData(
          show: true,
          topTitles: AxisTitles(
            sideTitles: SideTitles(showTitles: false),
          ),
          rightTitles: AxisTitles(
            sideTitles: SideTitles(showTitles: false),
          ),
        ),
        gridData: FlGridData(show: true),
        borderData: FlBorderData(show: false),
      ),
    );
  }
}
