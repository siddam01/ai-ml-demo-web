import 'package:flutter/material.dart';

import '../core/session_store.dart';
import '../network/rentflow_api.dart';
import 'properties_screen.dart';
import 'reports_screen.dart';
import 'settings_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key, required this.store});
  final SessionStore store;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _tab = 0;

  RentFlowApi get api => RentFlowApi(widget.store.api);

  @override
  Widget build(BuildContext context) {
    final pages = [
      PropertiesScreen(api: api),
      ReportsScreen(api: api),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('RentFlow'),
        actions: [
          IconButton(
            onPressed: () async {
              await Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => SettingsScreen(store: widget.store)),
              );
              setState(() {});
            },
            icon: const Icon(Icons.settings),
          ),
          IconButton(
            onPressed: () async {
              await widget.store.logout();
            },
            icon: const Icon(Icons.logout),
          ),
        ],
      ),
      body: pages[_tab],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tab,
        onDestinationSelected: (i) => setState(() => _tab = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_work), label: 'Properties'),
          NavigationDestination(icon: Icon(Icons.assessment), label: 'Reports'),
        ],
      ),
    );
  }
}

