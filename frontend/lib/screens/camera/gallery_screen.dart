import 'package:flutter/material.dart';

class GalleryScreen extends StatelessWidget {
  final List<String> imageList = [
    'lib/assets/images/logo.jpg',
  ];

  @override
  Widget build(BuildContext context) {
    final int crossAxisCount = 3;
    final double gridSpacing = 4.0;
    final double borderSize = 1.0;

    final int totalCells = crossAxisCount * 10; 

    return Scaffold(
      appBar: AppBar(
        title: Text('갤러리'),
        backgroundColor: Color(0xFFBBBBEE),
      ),
      body: GridView.builder(
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: crossAxisCount,
          crossAxisSpacing: gridSpacing,
          mainAxisSpacing: gridSpacing,
        ),
        itemCount: totalCells,
        itemBuilder: (BuildContext context, int index) {
          return Container(
            decoration: BoxDecoration(
              border: Border.all(
                color: Colors.grey, 
                width: borderSize,
              ),
            ),
            child: index < imageList.length
                ? Image.asset(
                    imageList[index],
                    fit: BoxFit.cover,
                  )
                : null, 
          );
        },
      ),
    );
  }
}
