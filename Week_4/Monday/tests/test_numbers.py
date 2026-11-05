"""Tests for celsius_to_fahrenheit and letter_grade (function-style tests)."""
import pytest

import sys

from qe_utils import celsius_to_fahrenheit, letter_grade


# ---- WORKED EXAMPLE ----
@pytest.mark.smoke
def test_freezing_point_converts_to_32f():
    assert celsius_to_fahrenheit(0) == 32


# ---- TODO tests ----

@pytest.mark.regression
def test_boiling_point_converts_to_212f():
    # TODO (Task 3): 100 C -> 212 F. Marker: regression
    
    # Arrange
    celsius = 100

    # Act
    result = celsius_to_fahrenheit(celsius)

    # Assert
    assert result == 212


@pytest.mark.regression
def test_body_temperature_uses_approx():
    # TODO (Task 4): 37 C is 98.6 F. Compare with pytest.approx, NOT ==. Marker: regression
    
    # Arrange
    celsius = 37

    # Act
    result = celsius_to_fahrenheit(celsius)

    # Assert
    assert result == pytest.approx(98.6)


@pytest.mark.boundary
def test_minus_40_is_same_in_both_scales():
    # TODO (Task 3): celsius_to_fahrenheit(-40) == -40. Marker: boundary
    
    # Arrange
    celsius = -40

    # Act
    result = celsius_to_fahrenheit(celsius)

    # Assert
    assert result == -40


@pytest.mark.smoke
@pytest.mark.boundary
def test_grade_90_is_a():
    # TODO (Task 3): boundary 90 -> "A". Markers: boundary, smoke
    
    # Arrange
    grade = 90

    # Act
    result = letter_grade(grade)

    # Assert
    assert result == 'A'


@pytest.mark.boundary
def test_grade_89_is_b():
    # TODO (Task 3): just below 90 -> "B". Marker: boundary
    
    # Arrange
    grade = 89

    # Act
    result = letter_grade(grade)

    # Assert
    assert result == 'B'


@pytest.mark.boundary
def test_grade_0_is_f_and_100_is_a():
    # TODO (Task 3): the two extreme valid scores. Marker: boundary
    
    # Arrange
    grade_min = 0
    grade_max = 100

    # Act
    result1 = letter_grade(grade_min)
    result2 = letter_grade(grade_max)

    # Assert
    assert result1 == 'F'
    assert result2 == 'A'


@pytest.mark.regression
def test_grade_below_zero_raises_value_error():
    # TODO (Task 4): -1 -> ValueError (check message with match=). Marker: regression
    
    # Arrange
    grade = -1

    # Act and Assert
    with pytest.raises(ValueError, match = "score must be between 0 and 100"):
        letter_grade(grade)


@pytest.mark.regression
def test_grade_above_100_raises_value_error():
    # TODO (Task 4): 101 -> ValueError. Marker: regression
    
    # Arrange
    grade = 101

    # Act and Assert
    with pytest.raises(ValueError, match = "score must be between 0 and 100"):
        letter_grade(grade)


# TODO (Task 5): add ONE test that uses @pytest.mark.skipif on a condition, e.g.
#   @pytest.mark.skipif(sys.version_info < (3, 8), reason="needs Python 3.8+")
# (import sys at the top). Any simple, truthful test is fine. Name it test_..._skipif_example.

@pytest.mark.skipif(
    sys.version_info < (3, 8),
    reason="needs Python 3.8+"
)
def test_letter_grade_skipif_example():
    # Arrange
    score = 70

    # Act
    result = letter_grade(score)

    # Assert
    assert result == "C"