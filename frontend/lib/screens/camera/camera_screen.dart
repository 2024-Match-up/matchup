import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'body_scan.dart';
import 'gallery_screen.dart';

class CameraScreen extends StatelessWidget {
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
              'Match up!',
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
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => BodyScanScreen()),
                        );
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
