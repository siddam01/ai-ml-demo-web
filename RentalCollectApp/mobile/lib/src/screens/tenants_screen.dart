import 'package:flutter/material.dart';

import '../models/models.dart';
import '../network/api_client.dart';
import '../network/rentflow_api.dart';
import 'payments_screen.dart';

class TenantsScreen extends StatefulWidget {
  const TenantsScreen({super.key, required this.api, required this.unit});
  final RentFlowApi api;
  final UnitPublic unit;

  @override
  State<TenantsScreen> createState() => _TenantsScreenState();
}

class _TenantsScreenState extends State<TenantsScreen> {
  late Future<List<TenantPublic>> _future;

  @override
  void initState() {
    super.initState();
    _future = widget.api.listTenants(widget.unit.id);
  }

  Future<void> _refresh() async {
    setState(() => _future = widget.api.listTenants(widget.unit.id));
    await _future;
  }

  Future<void> _createTenant() async {
    final nameCtrl = TextEditingController();
    final mobileCtrl = TextEditingController();
    final depositCtrl = TextEditingController(text: '0');
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('New Tenant'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Tenant name')),
            const SizedBox(height: 8),
            TextField(
              controller: mobileCtrl,
              decoration: const InputDecoration(labelText: 'Mobile'),
              keyboardType: TextInputType.phone,
            ),
            const SizedBox(height: 8),
            TextField(
              controller: depositCtrl,
              decoration: const InputDecoration(labelText: 'Deposit (optional)'),
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
      await widget.api.createTenant(
        unitId: widget.unit.id,
        name: nameCtrl.text.trim(),
        mobile: mobileCtrl.text.trim(),
        deposit: depositCtrl.text.trim().isEmpty ? null : depositCtrl.text.trim(),
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
      appBar: AppBar(title: Text('Tenants • ${widget.unit.unitName}')),
      body: FutureBuilder<List<TenantPublic>>(
        future: _future,
        builder: (context, snap) {
          final loading = snap.connectionState != ConnectionState.done;
          final items = snap.data ?? const <TenantPublic>[];
          return RefreshIndicator(
            onRefresh: _refresh,
            child: ListView(
              padding: const EdgeInsets.all(12),
              children: [
                Row(
                  children: [
                    Text('Tenants', style: Theme.of(context).textTheme.titleLarge),
                    const Spacer(),
                    FilledButton.icon(
                      onPressed: loading ? null : _createTenant,
                      icon: const Icon(Icons.person_add),
                      label: const Text('Add'),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                if (loading) const LinearProgressIndicator(),
                if (!loading && snap.hasError)
                  Text('Failed to load: ${snap.error}', style: const TextStyle(color: Colors.red)),
                for (final t in items)
                  Card(
                    child: ListTile(
                      title: Text(t.tenantName),
                      subtitle: Text(t.mobile),
                      trailing: const Icon(Icons.payments),
                      onTap: () async {
                        await Navigator.of(context).push(
                          MaterialPageRoute(builder: (_) => PaymentsScreen(api: widget.api, tenant: t)),
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

