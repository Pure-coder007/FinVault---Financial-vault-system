# FinVault---Financial-vault-system


# Wallet API Endpoints

## User Authentication
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/register/` | Register a new user |
| **POST** | `/login/` | Authenticate & get JWT token |
| **POST** | `/logout/` | Logout user and invalidate token |
| **POST** | `/enable-2fa/` | Enable Two-Factor Authentication (2FA) |
| **POST** | `/disable-2fa/` | Disable 2FA |
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
| **POST** | `/wallet/set-limit/` | Set custom transaction limits |

## Card Management
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/cards/add/` | Add a new payment card |
| **DELETE** | `/cards/remove/{card_id}/` | Remove a payment card |
| **GET** | `/cards/list/` | List all saved payment cards |
| **POST** | `/cards/set-default/{card_id}/` | Set a default payment card |

## Transactions
| Method | Endpoint | Description |
|--------|----------|------------|
| **GET** | `/transactions/` | Get transaction history (filter by date/type) |
| **POST** | `/transactions/reverse/` | Reverse a failed transaction |
| **GET** | `/transactions/status/{transaction_id}/` | Check transaction status |

## Payments
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/payment/request/` | Request money from another user |
| **POST** | `/payment/approve/` | Approve a payment request |
| **POST** | `/payment/reject/` | Reject a payment request |

## Bill Payments
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/bills/airtime/` | Buy airtime |
| **POST** | `/bills/electricity/` | Pay electricity bill |
| **POST** | `/bills/data/` | Buy data subscription |
| **POST** | `/bills/water/` | Pay water bill |
| **POST** | `/bills/internet/` | Pay internet subscription |

## Loan Services
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/loans/request/` | Request a loan |
| **POST** | `/loans/approve/` | Approve a loan request (Admin) |
| **POST** | `/loans/repay/` | Repay a loan |
| **GET** | `/loans/status/{loan_id}/` | Check loan status |
| **GET** | `/loans/history/` | Get loan repayment history |

## Webhooks
| Method | Endpoint | Description |
|--------|----------|------------|
| **POST** | `/webhooks/payment/` | Handle external payment webhook |
| **POST** | `/webhooks/loan-approval/` | Handle loan approval webhook |

## Admin Controls
| Method | Endpoint | Description |
|--------|----------|------------|
| **GET** | `/admin/users/` | Get all users (Admin only) |
| **GET** | `/admin/transactions/` | Get all transactions (Admin only) |
| **POST** | `/admin/freeze-wallet/` | Freeze a user’s wallet (Admin only) |
| **POST** | `/admin/unfreeze-wallet/` | Unfreeze a user’s wallet (Admin only) |
| **POST** | `/admin/block-user/` | Block a user account |
| **POST** | `/admin/unblock-user/` | Unblock a user account |

