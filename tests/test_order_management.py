import time
from time import sleep

import pytest
from dotenv import load_dotenv

from simulators.basket_simulator import BasketSimulator
from simulators.catalog_simulator import CatalogSimulator
from utils.messages.messages_generator import MessageGenerator

pytest.mark.parametrize()

load_dotenv()


def test_main_success_scenario():
    """
        Source Test Case Title: Verify the main success scenario for creating order is valid.
        Source Test Case Purpose: Verify that the submitting order functionality of the service is working.
        Source Test Case ID:1
        Source Test Case Traceability: 1.1.1
    """
    # Run steps 1-2
    test_user_can_submit_an_order()

    # Preparing test environment
    catalog_mock = CatalogSimulator()
    catalog_mock.purge_queue()
    mg = MessageGenerator()
    catalog_to_order_msg = mg.catalog_to_order(catalog_mock.CURRENT_ORDER_ID)

    # Step 3 - Verify that the catalog queue received the message from the ordering service.
    # Waiting for the queue to get the massage, and for the status to update for 'awaitingvalidation'.

    # Expected Result #3 - The catalog queue received the message from the ordering service, so the OrderStatusID in the orders table is updated to 2
    # The maximum time to wait for the order status to be updated is 30 seconds
    for i in range(30):
        # If the status is 2 - assert true
        if catalog_mock.verify_status_id_is_awaiting_validation():
            assert catalog_mock.verify_status_id_is_awaiting_validation()
        # If the status is not 2 - wait 2 second and try again
        else:
            time.sleep(1)

    # Finally, check if the status is 2 once again, if it is not, the test failed
    else:
        if not catalog_mock.verify_status_id_is_awaiting_validation():
            assert catalog_mock.verify_status_id_is_awaiting_validation()

    # Step #4 - Send from the catalog mock to the Ordering queue the massage to change status to 'stockconfirmed'.
    catalog_mock.validate_items_in_stock(catalog_to_order_msg["input"])

    # Expected Result #4 - The OrderStatusID in the orders table has been updated to 3.
    for i in range(30):
        # If the status is 3 - assert true
        if catalog_mock.verify_status_id_is_stock_confirmed():
            assert catalog_mock.verify_status_id_is_stock_confirmed()
        # If the status is not 3 - wait 2 second and try again
        else:
            time.sleep(1)
        # Finally, check if the status is 3 once again, if it is not, the test failed
    else:
        if not catalog_mock.verify_status_id_is_stock_confirmed:
            assert catalog_mock.verify_status_id_is_stock_confirmed()


def test_user_can_submit_an_order():
    """
        Source Test Case Title: Verify that the user can submit an order.
        Source Test Case Purpose: Verify that the submitting order functionality of the service is working.
        Source Test Case ID: 2
        Source Test Case Traceability: 1.2.1
    """
    # Preparing test environment
    basket_mock = BasketSimulator()
    basket_mock.purge_queue()
    sleep(2)
    mg = MessageGenerator()
    messages = mg.basket_to_order()

    # Step #1 - Send from the basket mock to the Ordering queue massage to create a new order.
    basket_mock.create_order(messages["input"])

    # Expected Result #1 - The basket queue received the correct output message (from the Message dictionary).
    expected_message = messages["output"]['UserId']
    actual_message = (basket_mock.get_first_message())['UserId']
    assert actual_message == expected_message

    # Step 2 - Verify that a new order entity has been created within the orders table, with OrderStatusID of 1.
    assert basket_mock.verify_status_id_is_submitted()
