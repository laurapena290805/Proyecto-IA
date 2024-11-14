import 'package:flutter/material.dart';

class AppStyles {
  static const Color primaryColor = Color.fromARGB(255, 105, 205, 210);
  static const Color secondaryColor = Color.fromARGB(255, 100, 196, 175);
  static const Color backgroundColor = Color(0xFFF6F6F6);
  static const Color buttonColor = Color(0xFFE0E0E0);

  static const TextStyle titleTextStyle = TextStyle(
    //tipo de fuente elegante para el encabezado
    fontFamily: 'Montserrat',
    fontSize: 50,
    fontWeight: FontWeight.bold,
    color: Colors.black,
  );

  static const TextStyle subtitleTextStyle = TextStyle(
    fontSize: 20,
    color: Colors.black,
  );

  static const TextStyle buttonTextStyle = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: Colors.black,
  );

  static const TextStyle infomationTextStyle = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w300,
    color: Colors.black,
  );
}
