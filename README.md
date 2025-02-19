# FinVault---Financial-vault-system


# Wallet API Endpoints

## User Authentication
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/register/` | Register a new user |
| **POST** | `/login/` | Authenticate & get JWT token |
| **POST** | `/logout/` | Logout user and invalidate token |
| **POST** | `/reset-password/` | Request password reset |
| **POST** | `/update-password/` | Update user password |

## Wallet Management
| Method | Endpoint | Description |
|--------|----------|------------|
| **GET** | `/wallet/balance/` | Get wallet balance |
| **POST** | `/wallet/fund/` | Add money to wallet (simulate card/bank funding) |
| **POST** | `/wallet/transfer/` | Transfer money to another user |
| **POST** | `/wallet/withdraw/` | Withdraw to a bank account |
| **POST** | `/wallet/lock-funds/` | Lock funds for savings |
| **POST** | `/wallet/unlock-funds/` | Withdraw locked savings after maturity |
| **GET** | `/wallet/limits/` | Get wallet transaction limits |
| **GET** | `/transactions/` | Get transaction history (filter by date/type) |


## Payments
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/payment/request/` | Request money from another user |
| **POST** | `/payment/approve/` | Approve a payment request |
| **POST** | `/payment/reject/` | Reject a payment request |


## Loan Services
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/loans/request/` | Request a loan |
| **POST** | `/loans/approve/` | Approve a loan request (Admin) |
| **POST** | `/loans/repay/` | Repay a loan |
| **GET** | `/loans/status/{loan_id}/` | Check loan status |
| **GET** | `/loans/history/` | Get loan repayment history |


## Admin Controls
| Method | Endpoint | Description |
|--------|----------|------------|
| **GET** | `/admin/users/` | Get all users (Admin only) |
| **GET** | `/admin/transactions/` | Get all transactions (Admin only) |
| **POST** | `/admin/freeze-wallet/` | Freeze a user’s wallet (Admin only) |
| **POST** | `/admin/unfreeze-wallet/` | Unfreeze a user’s wallet (Admin only) |
| **POST** | `/admin/block-user/` | Block a user account |
| **POST** | `/admin/unblock-user/` | Unblock a user account |

