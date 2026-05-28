import 'package:flutter/material.dart';

import 'core/app_theme.dart';
import 'core/session_store.dart';
import 'screens/dashboard_screen.dart';
import 'screens/login_screen.dart';

class RentFlowApp extends StatefulWidget {
  const RentFlowApp({super.key});

  @override
  State<RentFlowApp> createState() => _RentFlowAppState();
}

class _RentFlowAppState extends State<RentFlowApp> {
  final _store = SessionStore();
  bool _ready = false;

  @override
  void initState() {
    super.initState();
    _store.init().then((_) {
      setState(() => _ready = true);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!_ready) {
      return MaterialApp(
        theme: buildRentFlowTheme(),
        home: const Scaffold(body: Center(child: CircularProgressIndicator())),
      );
    }

    return ListenableBuilder(
      listenable: _store,
      builder: (context, _) {
        return MaterialApp(
          title: 'RentFlow',
          theme: buildRentFlowTheme(),
          home: _store.isAuthenticated
              ? DashboardScreen(store: _store)
              : LoginScreen(store: _store),
        );
      },
    );
  }
}

