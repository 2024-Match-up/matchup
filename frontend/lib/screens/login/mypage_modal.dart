import 'package:flutter/material.dart';
import '/services/api_client.dart';

final ApiClient apiClient = ApiClient();


void showMyPageModal(BuildContext context, String accessToken) {
  var screenWidth = MediaQuery.of(context).size.width;
  var screenHeight = MediaQuery.of(context).size.height;

  // Controllers
  final TextEditingController nicknameController = TextEditingController();
  final TextEditingController heightController = TextEditingController();
  final TextEditingController weightController = TextEditingController();

  String nickname = '';
  int height = 0;
  int weight = 0;

  bool profileExists = false;

  Future<void> fetchProfile() async {
    try {
      var profile = await apiClient.getProfile(accessToken);
      nickname = profile['nickname'] ?? '';
      height = profile['height'] ?? 0;
      weight = profile['weight'] ?? 0;

      nicknameController.text = nickname;
      heightController.text = height.toString();
      weightController.text = weight.toString();
      profileExists = true;
    } catch (e) {
      print('Failed to fetch profile: $e');
      profileExists = false;
    }
  }

  Future<void> createOrUpdateProfile(BuildContext context) async {
    try {
      nickname = nicknameController.text;
      height = int.tryParse(heightController.text) ?? 0;
      weight = int.tryParse(weightController.text) ?? 0;

      if (nickname.isNotEmpty && height > 0 && weight > 0) {
        if (profileExists) {
          await apiClient.updateProfile(nickname, height, weight, accessToken);
        } else {
          await apiClient.createProfile(nickname, height, weight, accessToken);
        }
      }
      Navigator.of(context).pop(); // Close the modal on success
    } catch (e) {
      print('Failed to update or create profile: $e');
    }
  }

  fetchProfile().then((_) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(builder: (context, setState) {
          return Dialog(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(screenWidth * 0.05),
            ),
            child: Padding(
              padding: EdgeInsets.all(screenWidth * 0.05),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Text(
                    '내 프로필',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: screenHeight * 0.03,
                    ),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextField(
                    controller: nicknameController,
                    textAlignVertical: TextAlignVertical.center,
                    decoration: InputDecoration(
                      hintText: '닉네임',
                      contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.02),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0)),
                    ),
                    onChanged: (value) => setState(() => nickname = value),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextField(
                    controller: heightController,
                    textAlignVertical: TextAlignVertical.center,
                    decoration: InputDecoration(
                      hintText: '신장',
                      contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.02),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0)),
                    ),
                    keyboardType: TextInputType.number,
                    onChanged: (value) => setState(() => height = int.tryParse(value) ?? height),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextField(
                    controller: weightController,
                    textAlignVertical: TextAlignVertical.center,
                    decoration: InputDecoration(
                      hintText: '몸무게',
                      contentPadding: EdgeInsets.symmetric(horizontal: screenWidth * 0.02),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10.0)),
                    ),
                    keyboardType: TextInputType.number,
                    onChanged: (value) => setState(() => weight = int.tryParse(value) ?? weight),
                  ),
                  SizedBox(height: screenHeight * 0.02),
                  TextButton(
                    child: Text('확인', style: TextStyle(fontSize: screenWidth * 0.04)),
                    style: TextButton.styleFrom(
                      foregroundColor: Colors.black,
                      backgroundColor: Color(0xFFBBBBEE),
                      minimumSize: Size(double.infinity, screenHeight * 0.06),
                      padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.03),
                    ),
                    onPressed: () => createOrUpdateProfile(context),
                  ),
                ],
              ),
            ),
          );
        });
      },
    );
  });
}

