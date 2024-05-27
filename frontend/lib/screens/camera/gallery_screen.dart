import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart';
import 'package:matchup/models/UserProvider.dart';
import 'image_viewer.dart';

class GalleryScreen extends StatefulWidget {
  @override
  _GalleryScreenState createState() => _GalleryScreenState();
}

class _GalleryScreenState extends State<GalleryScreen> {
  List<String> imageList = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchImages();
  }

  Future<void> fetchImages() async {
    final String baseUrl = 'http://172.30.1.1:8000/api/v1';
    final userProvider = Provider.of<UserProvider>(context, listen: false);
    final token = userProvider.accessToken;

    if (token == null) {
      print('Token is null');
      setState(() {
        isLoading = false;
      });
      return;
    }

    try {
      final response = await http.get(
        Uri.parse("$baseUrl/health/image"),
        headers: {
          'Authorization': 'Bearer $token',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        List<String> images = [];
        for (var entry in data['images']) {
          String? frontUrl = entry['front_url'];
          String? sideUrl = entry['side_url'];
          if (frontUrl != null && frontUrl != "url") {
            images.add(frontUrl);
          }
          if (sideUrl != null && sideUrl != "url") {
            images.add(sideUrl);
          }
        }
        setState(() {
          imageList = images;
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load images');
      }
    } catch (e) {
      print('Error fetching images: $e');
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final int crossAxisCount = 3;
    final double gridSpacing = 4.0;
    final double borderSize = 1.0;

    return Scaffold(
      appBar: AppBar(
        title: Text('갤러리'),
        backgroundColor: Color(0xFFBBBBEE),
      ),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : GridView.builder(
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: crossAxisCount,
                crossAxisSpacing: gridSpacing,
                mainAxisSpacing: gridSpacing,
              ),
              itemCount: imageList.length,
              itemBuilder: (BuildContext context, int index) {
                return GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ImageViewer(
                          imageList: imageList,
                          initialIndex: index,
                        ),
                      ),
                    );
                  },
                  child: Container(
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: Colors.grey,
                        width: borderSize,
                      ),
                    ),
                    child: Image.network(
                      imageList[index],
                      fit: BoxFit.cover,
                    ),
                  ),
                );
              },
            ),
    );
  }
}


