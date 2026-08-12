"""
Utility script to process a list of customer orders and compute totals
(fixed / production-ready version).
"""

import json
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderProcessingError(Exception):
    """Raised when an order cannot be processed due to invalid data."""


def load_orders(filename: str) -> list[dict]:
    """Load and parse orders from a JSON file."""
    with open(filename) as f:
        return json.load(f)


def calculate_total(order: dict, discounts: Optional[list[float]] = None) -> float:
    """Calculate the total price for an order, applying any discounts."""
    if discounts is None:
        discounts = []

    if "items" not in order:
        raise OrderProcessingError(f"Order {order.get('id', '?')} missing 'items'")

    total = 0.0
    for item in order["items"]:
        try:
            price = float(item["price"])
            qty = float(item["qty"])
        except (KeyError, TypeError, ValueError) as e:
            raise OrderProcessingError(
                f"Order {order.get('id', '?')} has invalid item data: {e}"
            ) from e
        total += price * qty

    for discount in discounts:
        total -= discount

    return max(total, 0.0)


def process_orders(filename: str) -> list[dict]:
    """Process all orders in a file and return their computed totals."""
    orders = load_orders(filename)
    results = []

    for order in orders:
        try:
            total = calculate_total(order)
            results.append({"id": order["id"], "total": total})
        except OrderProcessingError as e:
            logger.warning("Skipping order: %s", e)
        except KeyError as e:
            logger.warning("Order missing required field %s, skipping", e)

    return results


def apply_discount_code(order: dict, code: str) -> float:
    """Calculate an order's total after applying a discount code."""
    discount_map = {"SAVE10": 10, "SAVE20": 20}
    discounts = [discount_map[code]] if code in discount_map else []
    return calculate_total(order, discounts)


def summarize(results: list[dict]) -> None:
    """Print the total and average of all processed order results."""
    if not results:
        print("No orders to summarize.")
        return

    total_sum = sum(r["total"] for r in results)
    average = total_sum / len(results)
    print(f"Total: {total_sum}")
    print(f"Average: {average:.2f}")


def main() -> None:
    results = process_orders("orders.json")
    summarize(results)


if __name__ == "__main__":
    main()
