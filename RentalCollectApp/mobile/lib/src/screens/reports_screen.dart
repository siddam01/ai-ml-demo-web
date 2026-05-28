import 'package:flutter/material.dart';

import '../models/models.dart';
import '../network/rentflow_api.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key, required this.api});
  final RentFlowApi api;

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  late Future<List<TenantDue>> _future;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<List<TenantDue>> _load() async {
    final now = DateTime.now();
    final asOf = '${now.year.toString().padLeft(4, '0')}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')}';
    return widget.api.pendingDues(asOfIso: asOf);
  }

  Future<void> _refresh() async {
    setState(() => _future = _load());
    await _future;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<TenantDue>>(
      future: _future,
      builder: (context, snap) {
        final loading = snap.connectionState != ConnectionState.done;
        final items = snap.data ?? const <TenantDue>[];
        return RefreshIndicator(
          onRefresh: _refresh,
          child: ListView(
            padding: const EdgeInsets.all(12),
            children: [
              Row(
                children: [
                  Text('Pending Dues', style: Theme.of(context).textTheme.titleLarge),
                  const Spacer(),
                  IconButton(onPressed: loading ? null : _refresh, icon: const Icon(Icons.refresh)),
                ],
              ),
              const SizedBox(height: 8),
              if (loading) const LinearProgressIndicator(),
              if (!loading && snap.hasError) ...[
                Text('Failed to load: ${snap.error}', style: const TextStyle(color: Colors.red)),
                const SizedBox(height: 12),
              ],
              for (final d in items)
                Card(
                  child: ListTile(
                    title: Text('${d.tenantName} • ${d.dueAmountEstimate}'),
                    subtitle: Text('${d.propertyName} / ${d.unitName} (rent ${d.monthlyRent})'),
                  ),
                ),
              if (!loading && items.isEmpty)
                const Padding(
                  padding: EdgeInsets.only(top: 24),
                  child: Text('No dues found.'),
                ),
            ],
          ),
        );
      },
    );
  }
}

