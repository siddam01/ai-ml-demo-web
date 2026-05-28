import 'package:flutter/material.dart';

import '../models/models.dart';
import '../network/api_client.dart';
import '../network/rentflow_api.dart';
import 'units_screen.dart';

class PropertiesScreen extends StatefulWidget {
  const PropertiesScreen({super.key, required this.api});
  final RentFlowApi api;

  @override
  State<PropertiesScreen> createState() => _PropertiesScreenState();
}

class _PropertiesScreenState extends State<PropertiesScreen> {
  late Future<List<PropertyPublic>> _future;

  @override
  void initState() {
    super.initState();
    _future = widget.api.listProperties();
  }

  Future<void> _refresh() async {
    setState(() => _future = widget.api.listProperties());
    await _future;
  }

  Future<void> _createProperty() async {
    final nameCtrl = TextEditingController();
    final addrCtrl = TextEditingController();
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('New Property'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Property name')),
            const SizedBox(height: 8),
            TextField(controller: addrCtrl, decoration: const InputDecoration(labelText: 'Address (optional)')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Create')),
        ],
      ),
    );
    if (ok != true) return;

    try {
      await widget.api.createProperty(name: nameCtrl.text.trim(), address: addrCtrl.text.trim().isEmpty ? null : addrCtrl.text.trim());
      await _refresh();
    } on ApiException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed (${e.statusCode})')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<PropertyPublic>>(
      future: _future,
      builder: (context, snap) {
        final loading = snap.connectionState != ConnectionState.done;
        final items = snap.data ?? const <PropertyPublic>[];

        return RefreshIndicator(
          onRefresh: _refresh,
          child: ListView(
            padding: const EdgeInsets.all(12),
            children: [
              Row(
                children: [
                  Text('Properties', style: Theme.of(context).textTheme.titleLarge),
                  const Spacer(),
                  FilledButton.icon(
                    onPressed: loading ? null : _createProperty,
                    icon: const Icon(Icons.add),
                    label: const Text('Add'),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              if (loading) const LinearProgressIndicator(),
              if (!loading && snap.hasError)
                Text('Failed to load: ${snap.error}', style: const TextStyle(color: Colors.red)),
              for (final p in items)
                Card(
                  child: ListTile(
                    title: Text(p.propertyName),
                    subtitle: p.address == null ? null : Text(p.address!),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () async {
                      await Navigator.of(context).push(
                        MaterialPageRoute(builder: (_) => UnitsScreen(api: widget.api, property: p)),
                      );
                      await _refresh();
                    },
                  ),
                ),
            ],
          ),
        );
      },
    );
  }
}

