class PropertyPublic {
  PropertyPublic({required this.id, required this.propertyName, this.address});

  final String id;
  final String propertyName;
  final String? address;

  factory PropertyPublic.fromJson(Map<String, dynamic> json) => PropertyPublic(
        id: json['id'] as String,
        propertyName: json['property_name'] as String,
        address: json['address'] as String?,
      );
}

class UnitPublic {
  UnitPublic({required this.id, required this.unitName, required this.rentAmount});

  final String id;
  final String unitName;
  final String rentAmount;

  factory UnitPublic.fromJson(Map<String, dynamic> json) => UnitPublic(
        id: json['id'] as String,
        unitName: json['unit_name'] as String,
        rentAmount: json['rent_amount'].toString(),
      );
}

class TenantPublic {
  TenantPublic({required this.id, required this.tenantName, required this.mobile, this.deposit});

  final String id;
  final String tenantName;
  final String mobile;
  final String? deposit;

  factory TenantPublic.fromJson(Map<String, dynamic> json) => TenantPublic(
        id: json['id'] as String,
        tenantName: json['tenant_name'] as String,
        mobile: json['mobile'] as String,
        deposit: json['deposit']?.toString(),
      );
}

class PaymentPublic {
  PaymentPublic({required this.id});
  final String id;

  factory PaymentPublic.fromJson(Map<String, dynamic> json) => PaymentPublic(id: json['id'] as String);
}

class TenantDue {
  TenantDue({
    required this.tenantName,
    required this.propertyName,
    required this.unitName,
    required this.dueAmountEstimate,
    required this.monthlyRent,
  });

  final String tenantName;
  final String propertyName;
  final String unitName;
  final String dueAmountEstimate;
  final String monthlyRent;

  factory TenantDue.fromJson(Map<String, dynamic> json) => TenantDue(
        tenantName: json['tenant_name'] as String,
        propertyName: json['property_name'] as String,
        unitName: json['unit_name'] as String,
        dueAmountEstimate: json['due_amount_estimate'].toString(),
        monthlyRent: json['monthly_rent'].toString(),
      );
}

