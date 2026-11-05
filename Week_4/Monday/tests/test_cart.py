
"""Tests for calculate_cart_total (class-style tests)."""
import pytest

from qe_utils import calculate_cart_total


@pytest.mark.regression
class TestCartTotal:
    # ---- WORKED EXAMPLE ----
    @pytest.mark.smoke
    def test_total_of_two_items_without_tax(self):
        assert calculate_cart_total([10.00, 5.50]) == 15.50

    # ---- TODO tests ----

    @pytest.mark.smoke
    def test_total_with_ten_percent_tax(self):
        # Arrange
        prices = [100.00]
        tax_rate = 0.10

        # Act
        result = calculate_cart_total(prices, tax_rate)

        # Assert
        assert result == 110.0

    @pytest.mark.boundary
    def test_empty_cart_total_is_zero(self):
        # Arrange
        prices = []

        # Act
        result = calculate_cart_total(prices)

        # Assert
        assert result == 0

    def test_total_is_rounded_to_two_decimals(self):
        # Arrange
        prices = [19.99, 0.01, 3.333]
        tax_rate = 0.07

        # Act
        result = calculate_cart_total(prices, tax_rate)

        # Assert
        assert result == pytest.approx(24.97, abs=0.01)

    def test_negative_price_raises_value_error(self):
        # Arrange
        prices = [5.0, -1.0]

        # Act and Assert
        with pytest.raises(ValueError, match="negative"):
            calculate_cart_total(prices)

    def test_negative_tax_rate_raises_value_error(self):
        # Arrange
        prices = [5.0]
        tax_rate = -0.1

        # Act and Assert
        with pytest.raises(ValueError, match="tax_rate"):
            calculate_cart_total(prices, tax_rate)

    @pytest.mark.slow
    def test_large_cart_of_10000_items(self):
        # Arrange
        prices = [1.0] * 10_000

        # Act
        result = calculate_cart_total(prices)

        # Assert
        assert result == 10000.0

    @pytest.mark.skip(reason="coupons not implemented, see backlog")
    def test_discount_coupons_not_supported_yet(self):
        assert False
