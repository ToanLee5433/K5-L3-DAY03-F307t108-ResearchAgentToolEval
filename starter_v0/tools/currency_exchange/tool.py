from __future__ import annotations

from typing import Any

from tools._shared import err

# Bảng tỷ giá hối đoái chuẩn hóa (tham chiếu trên 1 USD)
EXCHANGE_RATES_TO_USD: dict[str, float] = {
    "USD": 1.0,
    "VND": 25450.0,
    "EUR": 0.92,
    "JPY": 155.2,
    "GBP": 0.79,
    "CNY": 7.24,
    "SGD": 1.35,
    "KRW": 1390.0,
}


def convert_currency(
    base_currency: str = "USD",
    target_currency: str = "VND",
    amount: float = 1.0,
) -> dict[str, Any]:
    """Quy đổi giá trị tiền tệ giữa các đồng tiền phổ biến dựa trên tỷ giá thị trường."""
    try:
        base = (base_currency or "USD").strip().upper()
        target = (target_currency or "VND").strip().upper()

        if base not in EXCHANGE_RATES_TO_USD:
            raise ValueError(
                f"Đồng tiền nguồn '{base}' không được hỗ trợ. Các đồng tiền hỗ trợ: {sorted(EXCHANGE_RATES_TO_USD.keys())}"
            )
        if target not in EXCHANGE_RATES_TO_USD:
            raise ValueError(
                f"Đồng tiền đích '{target}' không được hỗ trợ. Các đồng tiền hỗ trợ: {sorted(EXCHANGE_RATES_TO_USD.keys())}"
            )

        try:
            val = float(amount)
        except (ValueError, TypeError) as conv_err:
            raise ValueError(f"Số tiền 'amount' không hợp lệ: {amount}") from conv_err

        if val < 0:
            raise ValueError(f"Số tiền quy đổi không được là số âm: {val}")

        # Tính tỷ giá chéo qua USD
        rate = EXCHANGE_RATES_TO_USD[target] / EXCHANGE_RATES_TO_USD[base]
        converted = round(val * rate, 2)

        return {
            "tool": "currency_exchange",
            "base_currency": base,
            "target_currency": target,
            "amount": val,
            "converted_amount": converted,
            "rate": round(rate, 4),
            "formatted": f"{val:,.2f} {base} = {converted:,.2f} {target} (tỷ giá: {rate:,.4f})",
        }
    except Exception as exc:
        return err("currency_exchange", exc)
