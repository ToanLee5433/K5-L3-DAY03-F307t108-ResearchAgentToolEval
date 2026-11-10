---
name: currency_exchange
track: bonus
kind: local_formatter
provider: internal
requires_env: []
inputs: [base_currency, target_currency, amount]
outputs: [base_currency, target_currency, amount, converted_amount, rate, formatted]
side_effect: false
---
# currency_exchange

Tra cứu tỷ giá hối đoái và quy đổi giá trị tiền tệ giữa các đồng tiền (USD, VND, EUR, JPY, GBP, CNY, SGD, KRW).
Dùng khi người dùng hỏi tỷ giá, đổi tiền, hoặc tính toán ngân sách bằng ngoại tệ.

