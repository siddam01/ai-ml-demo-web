import 'package:flutter/material.dart';

import '../core/session_store.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key, required this.store});
  final SessionStore store;

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late final TextEditingController _baseUrl;

  @override
  void initState() {
    super.initState();
    _baseUrl = TextEditingController(text: widget.store.baseUrl);
  }

  @override
  void dispose() {
    _baseUrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _baseUrl,
              decoration: const InputDecoration(
                labelText: 'API base URL',
                helperText: 'Example: http://10.0.2.2:8000/api/v1',
              ),
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: () {
                final nav = Navigator.of(context);
                final url = _baseUrl.text;
                widget.store.updateBaseUrl(url).then((_) {
                  if (!mounted) return;
                  nav.pop();
                });
              },
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}

