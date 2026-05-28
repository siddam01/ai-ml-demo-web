import 'package:flutter/material.dart';

import '../models/models.dart';
import '../network/api_client.dart';
import '../network/rentflow_api.dart';

class PaymentsScreen extends StatefulWidget {
  const PaymentsScreen({super.key, required this.api, required this.tenant});
  final RentFlowApi api;
  final TenantPublic tenant;

  @override
  State<PaymentsScreen> createState() => _PaymentsScreenState();
}

class _PaymentsScreenState extends State<PaymentsScreen> {
  bool _busy = false;

  Future<void> _createPayment() async {
    final amountCtrl = TextEditingController(text: '5000.00');
    final noteCtrl = TextEditingController();
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('New Payment'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: amountCtrl,
              decoration: const InputDecoration(labelText: 'Amount'),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 8),
            TextField(controller: noteCtrl, decoration: const InputDecoration(labelText: 'Note (optional)')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Save')),
        ],
      ),
    );
    if (ok != true) return;

    setState(() => _busy = true);
    try {
      final today = DateTime.now();
      final iso = '${today.year.toString().padLeft(4, '0')}-${today.month.toString().padLeft(2, '0')}-${today.day.toString().padLeft(2, '0')}';
      await widget.api.createPayment(
        tenantId: widget.tenant.id,
        amount: amountCtrl.text.trim(),
        paymentDateIso: iso,
        note: noteCtrl.text.trim().isEmpty ? null : noteCtrl.text.trim(),
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Payment saved')));
    } on ApiException catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed (${e.statusCode})')));
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Payments • ${widget.tenant.tenantName}')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('This is a minimal skeleton: create payments only.', style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 12),
            FilledButton.icon(
              onPressed: _busy ? null : _createPayment,
              icon: const Icon(Icons.add),
              label: const Text('Add Payment'),
            ),
          ],
        ),
      ),
    );
  }
}

