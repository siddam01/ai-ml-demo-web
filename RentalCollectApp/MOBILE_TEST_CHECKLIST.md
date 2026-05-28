# Mobile (Android Emulator) E2E Checklist

## Preconditions

- Backend running on your PC:
  - Swagger: `http://127.0.0.1:8000/api/v1/docs`
- For Android emulator, base URL must be:
  - `http://10.0.2.2:8000/api/v1`

## 1. Start backend

From `RentalCollectApp/backend`:

```powershell
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 2. Start Flutter app

From `RentalCollectApp/mobile`:

```powershell
flutter run
```

If you see a symlink / developer mode error on Windows, enable Developer Mode:

```powershell
start ms-settings:developers
```

## 3. Configure API URL in app

- Open **Settings** (gear icon on login screen)
- Set **API base URL** to: `http://10.0.2.2:8000/api/v1`
- Save

## 4. Auth flow

- Register a new Owner (name/mobile/password)
- Login with same mobile/password
- Confirm you land on Dashboard

## 5. Properties → Units → Tenants → Payments

- Properties tab
  - Add Property
  - Tap Property → Units screen
  - Add Unit
  - Tap Unit → Tenants screen
  - Add Tenant
  - Tap Tenant → Payments screen
  - Add Payment

## 6. Reports

- Reports tab
- Confirm **Pending Dues** loads without errors

## Evidence (screenshots)

Capture these screenshots:

- Login screen showing configured base URL
- Register success
- Dashboard
- Property list + created property
- Unit list + created unit
- Tenant list + created tenant
- Payment saved toast
- Reports / pending dues list

