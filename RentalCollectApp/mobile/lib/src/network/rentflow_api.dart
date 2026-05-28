import '../models/models.dart';
import 'api_client.dart';

class RentFlowApi {
  RentFlowApi(this._api);
  final ApiClient _api;

  Future<List<PropertyPublic>> listProperties() async {
    final json = await _api.getJson('/properties');
    return (json as List).map((e) => PropertyPublic.fromJson(e as Map<String, dynamic>)).toList();
  }

  Future<PropertyPublic> createProperty({required String name, String? address}) async {
    final json = await _api.postJson('/properties', {'property_name': name, 'address': address});
    return PropertyPublic.fromJson(json as Map<String, dynamic>);
  }

  Future<List<UnitPublic>> listUnits(String propertyId) async {
    final json = await _api.getJson('/properties/$propertyId/units');
    return (json as List).map((e) => UnitPublic.fromJson(e as Map<String, dynamic>)).toList();
  }

  Future<UnitPublic> createUnit({required String propertyId, required String unitName, required String rentAmount}) async {
    final json = await _api.postJson('/properties/$propertyId/units', {
      'unit_name': unitName,
      'rent_amount': rentAmount,
    });
    return UnitPublic.fromJson(json as Map<String, dynamic>);
  }

  Future<List<TenantPublic>> listTenants(String unitId) async {
    final json = await _api.getJson('/tenants', query: {'unit_id': unitId});
    return (json as List).map((e) => TenantPublic.fromJson(e as Map<String, dynamic>)).toList();
  }

  Future<TenantPublic> createTenant({
    required String unitId,
    required String name,
    required String mobile,
    String? deposit,
  }) async {
    final json = await _api.postJson('/tenants', {
      'unit_id': unitId,
      'tenant_name': name,
      'mobile': mobile,
      'deposit': deposit,
    });
    return TenantPublic.fromJson(json as Map<String, dynamic>);
  }

  Future<PaymentPublic> createPayment({
    required String tenantId,
    required String amount,
    required String paymentDateIso,
    String status = 'paid',
    String? note,
  }) async {
    final json = await _api.postJson('/payments', {
      'tenant_id': tenantId,
      'amount': amount,
      'payment_date': paymentDateIso,
      'status': status,
      'note': note,
    });
    return PaymentPublic.fromJson(json as Map<String, dynamic>);
  }

  Future<List<TenantDue>> pendingDues({required String asOfIso}) async {
    final json = await _api.getJson('/reports/pending-dues', query: {'as_of': asOfIso});
    return (json as List).map((e) => TenantDue.fromJson(e as Map<String, dynamic>)).toList();
  }
}

