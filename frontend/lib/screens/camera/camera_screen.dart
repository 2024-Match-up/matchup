import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import 'body_scan.dart';
import 'gallery_screen.dart';
import 'package:matchup/models/UserProvider.dart';


final String baseUrl = 'http://13.124.114.252:8000/api/v1';
// final String baseUrl = 'http://10.254.3.138:8000/api/v1';


class CameraScreen extends StatelessWidget {
  Future<void> sendGetRequest(BuildContext context) async {
    final uri = Uri.parse("$baseUrl/health/init/");
    var request = http.MultipartRequest('GET', uri);

    final userProvider = Provider.of<UserProvider>(context, listen: false);
    final token = userProvider.accessToken;

    if (token != null) {
      print('Token: $token');
      request.headers['Authorization'] = 'Bearer $token';

      try {
        final response = await request.send();
        if (response.statusCode == 200) {
          print('Request successful');
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => BodyScanScreen()),
          );
        } else {
          print('Request failed with status: ${response.statusCode}');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Request failed with status: ${response.statusCode}')),
          );
        }
      } catch (e) {
        print('Request failed with error: $e');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Request failed with error: $e')),
        );
      }
    } else {
      print('Token is null');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Token is missing')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(screenWidth * 0.04),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            // 로고 이미지
            Image.asset(
              'lib/assets/images/logo.jpg',
              height: screenHeight * 0.25,
              fit: BoxFit.contain,
            ),
            Text(
              'Mobi-Move!',
              style: TextStyle(
                fontSize: screenWidth * 0.15,
                fontFamily: "Timmana",
                fontWeight: FontWeight.w300,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: screenHeight * 0.08),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Expanded(
                  child: Padding(
                    padding: EdgeInsets.only(right: screenWidth * 0.02),
                    child: ElevatedButton(
                      child: Text('체형 측정하기'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFFBBBBEE),
                        foregroundColor: Color(0xFF000000),
                        padding: EdgeInsets.symmetric(
                          horizontal: screenWidth * 0.08,
                          vertical: screenHeight * 0.02,
                        ),
                        textStyle: TextStyle(
                          fontSize: screenWidth * 0.04,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(screenWidth * 0.05),
                        ),
                      ),
                      onPressed: () {
                        sendGetRequest(context);
                      },
                    ),
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: EdgeInsets.only(left: screenWidth * 0.02),
                    child: ElevatedButton(
                      child: Text('갤러리'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFFBBBBEE),
                        foregroundColor: Color(0xFF000000),
                        padding: EdgeInsets.symmetric(
                          horizontal: screenWidth * 0.08,
                          vertical: screenHeight * 0.02,
                        ),
                        textStyle: TextStyle(
                          fontSize: screenWidth * 0.04,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(screenWidth * 0.05),
                        ),
                      ),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => GalleryScreen()),
                        );
                      },
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
