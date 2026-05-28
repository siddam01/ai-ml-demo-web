import 'package:flutter/material.dart';

import '../models/models.dart';
import '../network/api_client.dart';
import '../network/rentflow_api.dart';
import 'tenants_screen.dart';

class UnitsScreen extends StatefulWidget {
  const UnitsScreen({super.key, required this.api, required this.property});
  final RentFlowApi api;
  final PropertyPublic property;

  @override
  State<UnitsScreen> createState() => _UnitsScreenState();
}

class _UnitsScreenState extends State<UnitsScreen> {
  late Future<List<UnitPublic>> _future;

  @override
  void initState() {
    super.initState();
    _future = widget.api.listUnits(widget.property.id);
  }

  Future<void> _refresh() async {
    setState(() => _future = widget.api.listUnits(widget.property.id));
    await _future;
  }

  Future<void> _createUnit() async {
    final nameCtrl = TextEditingController();
    final rentCtrl = TextEditingController(text: '5000.00');
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('New Unit'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Unit name')),
            const SizedBox(height: 8),
            TextField(
              controller: rentCtrl,
              decoration: const InputDecoration(labelText: 'Monthly rent'),
              keyboardType: TextInputType.number,
            ),
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
      await widget.api.createUnit(
        propertyId: widget.property.id,
        unitName: nameCtrl.text.trim(),
        rentAmount: rentCtrl.text.trim(),
      );
      await _refresh();
    } on ApiException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed (${e.statusCode})')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Units • ${widget.property.propertyName}')),
      body: FutureBuilder<List<UnitPublic>>(
        future: _future,
        builder: (context, snap) {
          final loading = snap.connectionState != ConnectionState.done;
          final items = snap.data ?? const <UnitPublic>[];
          return RefreshIndicator(
            onRefresh: _refresh,
            child: ListView(
              padding: const EdgeInsets.all(12),
              children: [
                Row(
                  children: [
                    Text('Units', style: Theme.of(context).textTheme.titleLarge),
                    const Spacer(),
                    FilledButton.icon(
                      onPressed: loading ? null : _createUnit,
                      icon: const Icon(Icons.add),
                      label: const Text('Add'),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                if (loading) const LinearProgressIndicator(),
                if (!loading && snap.hasError)
                  Text('Failed to load: ${snap.error}', style: const TextStyle(color: Colors.red)),
                for (final u in items)
                  Card(
                    child: ListTile(
                      title: Text(u.unitName),
                      subtitle: Text('Rent: ${u.rentAmount}'),
                      trailing: const Icon(Icons.people),
                      onTap: () async {
                        await Navigator.of(context).push(
                          MaterialPageRoute(builder: (_) => TenantsScreen(api: widget.api, unit: u)),
                        );
                        await _refresh();
                      },
                    ),
                  ),
              ],
            ),
          );
        },
      ),
    );
  }
}

