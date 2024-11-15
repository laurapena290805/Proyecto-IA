import 'package:flutter/material.dart';
import 'pages/home.dart';

void main() {
  runApp(const AgentMouse());
}

class AgentMouse extends StatelessWidget {
  const AgentMouse({super.key});

  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: {
        '/': (context) => const HomeScreen(),
      },
    );
  }
}

