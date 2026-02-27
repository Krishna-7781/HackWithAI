import math


def staffing_recommendation(crowd):
    """
    1 staff per 20 guests
    Minimum 3 staff required
    """
    staff = math.ceil(crowd / 20)
    return max(staff, 3)


def menu_recommendation(crowd):
    """
    Assumptions:
    70% snacks
    50% beverages
    25% meals
    + 10% safety buffer
    """
    snacks = int(crowd * 0.7 * 1.1)
    drinks = int(crowd * 0.5 * 1.1)
    meals = int(crowd * 0.25 * 1.1)

    return snacks, drinks, meals


if __name__ == "__main__":
    test_crowd = 120
    print("Test for 120 people:")
    print("Staff:", staffing_recommendation(test_crowd))
    print("Menu:", menu_recommendation(test_crowd))