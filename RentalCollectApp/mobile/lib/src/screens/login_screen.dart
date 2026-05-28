import 'package:flutter/material.dart';

import '../core/session_store.dart';
import '../network/api_client.dart';
import 'settings_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key, required this.store});
  final SessionStore store;

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _mobile = TextEditingController();
  final _password = TextEditingController();
  bool _busy = false;
  String? _error;

  @override
  void dispose() {
    _mobile.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      final tokens = await widget.store.auth.login(mobile: _mobile.text.trim(), password: _password.text);
      await widget.store.setTokens(access: tokens.accessToken, refresh: tokens.refreshToken);
    } on ApiException catch (e) {
      setState(() => _error = 'Login failed (${e.statusCode})');
    } catch (e) {
      setState(() => _error = 'Login failed');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('RentFlow Login'),
        actions: [
          IconButton(
            onPressed: () async {
              await Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => SettingsScreen(store: widget.store)),
              );
              setState(() {});
            },
            icon: const Icon(Icons.settings),
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Base URL: ${widget.store.baseUrl}', style: Theme.of(context).textTheme.bodySmall),
              const SizedBox(height: 12),
              TextFormField(
                controller: _mobile,
                decoration: const InputDecoration(labelText: 'Mobile (10 digits)'),
                keyboardType: TextInputType.phone,
                validator: (v) => (v == null || v.trim().length < 10) ? 'Enter mobile' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _password,
                decoration: const InputDecoration(labelText: 'Password'),
                obscureText: true,
                validator: (v) => (v == null || v.trim().length < 8) ? 'Min 8 chars' : null,
              ),
              const SizedBox(height: 12),
              if (_error != null) Text(_error!, style: const TextStyle(color: Colors.red)),
              const SizedBox(height: 12),
              FilledButton(
                onPressed: _busy ? null : _login,
                child: _busy ? const CircularProgressIndicator() : const Text('Login'),
              ),
              const SizedBox(height: 8),
              OutlinedButton(
                onPressed: _busy
                    ? null
                    : () async {
                        await Navigator.of(context).push(MaterialPageRoute(
                          builder: (_) => RegisterScreen(store: widget.store),
                        ));
                      },
                child: const Text('Register (new owner)'),
              )
            ],
          ),
        ),
      ),
    );
  }
}

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key, required this.store});
  final SessionStore store;

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _mobile = TextEditingController();
  final _password = TextEditingController();
  bool _busy = false;
  String? _error;
  String? _success;

  @override
  void dispose() {
    _name.dispose();
    _mobile.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _register() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _busy = true;
      _error = null;
      _success = null;
    });
    try {
      final id = await widget.store.auth.register(
        name: _name.text.trim(),
        mobile: _mobile.text.trim(),
        password: _password.text,
      );
      setState(() => _success = 'Registered: $id');
    } on ApiException catch (e) {
      setState(() => _error = 'Register failed (${e.statusCode})');
    } catch (_) {
      setState(() => _error = 'Register failed');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register Owner')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller: _name,
                decoration: const InputDecoration(labelText: 'Name'),
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Enter name' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _mobile,
                decoration: const InputDecoration(labelText: 'Mobile'),
                keyboardType: TextInputType.phone,
                validator: (v) => (v == null || v.trim().length < 10) ? 'Enter mobile' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _password,
                decoration: const InputDecoration(labelText: 'Password'),
                obscureText: true,
                validator: (v) => (v == null || v.trim().length < 8) ? 'Min 8 chars' : null,
              ),
              const SizedBox(height: 12),
              if (_error != null) Text(_error!, style: const TextStyle(color: Colors.red)),
              if (_success != null) Text(_success!, style: const TextStyle(color: Colors.green)),
              const SizedBox(height: 12),
              FilledButton(
                onPressed: _busy ? null : _register,
                child: _busy ? const CircularProgressIndicator() : const Text('Create Owner'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

