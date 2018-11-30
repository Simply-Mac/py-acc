#######################################################################################################################
#
#  AppleCare Connect API Library Python 3.x Module
#
# Overview
# The purpose of this Python module is to provide a standard Python module to interact with the AppleCare Connect API.
# Each method in this function interacts seamlessly with the API and either returns data from the method call or a
# status message indicating the result of the API call
#
# API methods not yet implemented are:
# - Get POC Content
# - Get Consolidated POC
# - Device Configuration
# - Update Failed Authorization Status
#
# Dependencies
# - Python 3.x
# - 'requests' module
#
# Credits
# Big thanks to the folks that wrote the Meraki 'dashboard-api-python' module. This module borrowed a lot of from them.
#######################################################################################################################

import json
import os

import requests


def acc_credentials():
    """
    :usage: Defines the AppleCare Settings for the API calls
    :return: Requests Session w/ headers and ACC cert, ACC ShipTo, and endpoint base URL
    """
    # Begin a Requests Session for all API Calls
    session = requests.Session()
    session.headers.update({'Content-Type': "application/json;charset=utf-8"})

    # Get ACC Connection Details from Environment Variables
    acc_ship_to = os.environ['ACC_SHIPTO']  # AppleCare Connect 10 Digit SHIPTO Number
    acc_env = os.environ['ACC_ENV']  # AppleCare Connect Environment: UAT or PROD

    # Set the base_url of the AppleCare Connect endpoint and SSL cert
    # Default to ACC Application IPT Sandbox w/ UAT Cert
    base_url = "https://acc-ipt.apple.com/order-service/1.0"
    session.cert = (
        os.environ['ACC_UAT_CERT'],  # Path to AppleCare Connect UAT Cert .PEM File
        os.environ['ACC_UAT_PRIVATE_KEY']  # Path to AppleCare Connect UAT Private Key .PEM File
    )

    if acc_env == 'UAT':
        # Joint UAT environment
        session.cert = (
            os.environ['ACC_UAT_CERT'],  # Path to AppleCare Connect UAT Cert .PEM File
            os.environ['ACC_UAT_PRIVATE_KEY']  # Path to AppleCare Connect UAT Private Key .PEM File
        )
        if (int(acc_ship_to) % 2) == 0:
            base_url = "https://api-applecareconnect-ept.apple.com/order-service/1.0"
        else:
            base_url = "https://api-applecareconnect-ept2.apple.com/order-service/1.0"
    elif acc_env == 'PROD':
        # Production environment
        session.cert = (
            os.environ['ACC_PROD_CERT'],  # Path to AppleCare Connect PROD Cert .PEM File
            os.environ['ACC_PROD_PRIVATE_KEY']  # Path to AppleCare Connect PROD Private Key .PEM File
        )
        if (int(acc_ship_to) % 2) == 0:
            base_url = "https://api-applecareconnect.apple.com/order-service/1.0"
        else:
            base_url = "https://api-applecareconnect2.apple.com/order-service/1.0"

    return session, acc_ship_to, base_url


def is_json(json_array):
    """
    :param json_array: String variable to be validated if it is JSON
    :return: True if json_array is valid, False if not
    """
    try:
        json_object = json.loads(json_array)
    except ValueError:
        return False
    return True


def response_handler(full_response, suppress_print):
    """
    :param full_response: JSON response from the DEP API
    :param suppress_print: Prints output when function is called
    :return: Full API response and any API errors and their messages
    """
    valid_return = is_json(full_response)

    if valid_return:
        json_response = json.loads(full_response)
        error_code = []
        error_message = []

        # Verify/Create/Cancel Order Error
        if "orderErrorResponse" in full_response:
            api_errors = json_response["orderErrorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(json_response["orderErrorResponse"]["errorCode"])
                error_message.append(json_response["orderErrorResponse"]["errorMessage"])
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # Device Enrollment Error
        elif 'deviceErrorResponse' in full_response:
            api_errors = json_response["orderDetailsResponses"]["deviceEligibility"]["deviceErrorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(
                    json_response["orderDetailsResponses"]["deviceEligibility"]["deviceErrorResponse"]["errorCode"]
                )
                error_message.append(
                    json_response["orderDetailsResponses"]["deviceEligibility"]["deviceErrorResponse"]["errorMessage"]
                )
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # Order Lookup Error
        elif "lookupErrorResponse" in full_response:
            api_errors = json_response["lookupErrorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(
                    json_response["lookupErrorResponse"]["errorCode"]
                )
                error_message.append(
                    json_response["lookupErrorResponse"]["errorMessage"]
                )
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # POC Content Error
        elif "pocErrorResponse" in full_response:
            api_errors = json_response["pocErrorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(
                    json_response["pocErrorResponse"]["errorCode"]
                )
                error_message.append(
                    json_response["pocErrorResponse"]["errorMessage"]
                )
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # Device Configuration Error
        elif "deviceConfigErrorResponse" in full_response:
            api_errors = json_response["deviceConfigErrorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(
                    json_response["deviceConfigErrorResponse"]["errorCode"]
                )
                error_message.append(
                    json_response["deviceConfigErrorResponse"]["errorMessage"]
                )
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # Failed Auth Error
        elif "failedAuthErrorResponse" in full_response:
            api_errors = json_response["failedAuthErrorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(
                    json_response["failedAuthErrorResponse"]["errorCode"]
                )
                error_message.append(
                    json_response["failedAuthErrorResponse"]["errorMessage"]
                )
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # Consolidated POC Error
        elif "errorResponse" in full_response:
            api_errors = json_response["errorResponse"]
            if isinstance(api_errors, dict):
                # Single Error
                error_code.append(
                    json_response["errorResponse"]["errorCode"]
                )
                error_message.append(
                    json_response["errorResponse"]["errorMessage"]
                )
            else:
                # Multiple Errors
                for error in api_errors:
                    error_code.append(error["errorCode"])
                    error_message.append(error["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # Ship-to Error
        elif "error_code" in full_response:
            error_code.append(json_response["errorCode"])
            error_message.append(json_response["errorMessage"])
            if suppress_print is False:
                print('API Error: {0}'.format(error_code))
        # No Errors
        else:
            if suppress_print is False:
                print('REST Operation Successful - See full response for details\n')

    else:
        error_code = "ACC_ERR_0001"
        error_message = "JSON is invalid - Inspect full response for errors"
        if suppress_print is False:
            print('{}\n'.format(error_message))
            print(full_response)

    return json.loads(full_response), error_code, error_message


def verify_order(invoice_number, first_name, last_name, company_name, email_address, address_line1, address_line2, city,
                 state, zip_code, device_id, secondary_serial, purchase_date, suppress_print=False):
    """
    :usage: Designed to verify an order, to ensure that all criteria are met before placing the order. This API is
            recommended to be used before using the createOrder API.
    :param invoice_number: Invoice number from POS
    :param first_name: Customer's first name as shown on invoice
    :param last_name: Customer's last name as shown on invoice
    :param company_name: Customer's company as shown on invoice (optional)
    :param email_address: Customer's email address as shown on invoice
    :param address_line1: First line of Customer's street address as shown on invoice (optional)
    :param address_line2: Second line of Customer's street address as shown on invoice (optional)
    :param city: City of Customer's street address as shown on invoice (optional)
    :param state: State of Customer's street address as shown on invoice (optional)
    :param zip_code: Zip Code of Customer's street address as shown on invoice (optional)
    :param device_id: Serial number of the AppleCare eligible device sold
    :param secondary_serial: Serial number the secondary AppleCare eligible device sold (Thunderbolt Display, optional)
    :param purchase_date: Purchase date of the AppleCare eligible device
    :param suppress_print: Suppress any print output from function (Default: False)
    :return: JSON formatted strings of the complete API request, response, and any error codes
    """
    # Establish request variables
    session, acc_ship_to, base_url = acc_credentials()

    post_url = '{0}/verify-order/'.format(str(base_url))
    call_type = 'verify_order'

    # Create request array
    request_array = dict(shipTo=acc_ship_to, timeZone="420", langCode="en")

    # Customer Request array
    customer = dict(
        customerEmailId=email_address, address_line1=address_line1, address_line2=address_line2, city=city,
        stateCode=state, countryCode="US", zipCode=zip_code
    )
    # Use 'company_name' if 'first_name' and 'last_name' combined is longer than 34 characters
    full_name = '{0} {1}'.format(str(first_name), str(last_name))
    if len(full_name) > 34:
        customer['company_name'] = full_name
        customer['customerFirstName'] = ""
        customer['customerLastName'] = ""
    else:
        customer['company_name'] = company_name
        customer['customerFirstName'] = first_name
        customer['customerLastName'] = last_name

    # deviceRequest
    device = dict(
        deviceId=device_id.upper(), secondarySerialNumber=secondary_serial,
        hardwareDateOfPurchase=purchase_date, verifyMPN="", nsPart=""
    )

    # Prepare data in array
    post_data = dict(
        requestContext=request_array, customerRequest=customer, deviceRequest=device,
        appleCareSalesDate=purchase_date, pocLanguage="ENG", pocDeliveryPreference="E",
        purchaseOrderNumber=invoice_number, marketID="", overridePocFlag="", emailFlag="1"
    )

    # Format post_data as JSON
    full_request = json.dumps(post_data)

    # Send data to API
    response = session.post(post_url, data=full_request)

    # Call return handler function to parse request response
    full_response, error_code, error_message = response_handler(response.text, suppress_print)

    return post_data, full_response, error_code, error_message, call_type


def create_order(invoice_number, first_name, last_name, company_name, email_address, address_line1, address_line2, city,
                 state, zip_code, device_id, secondary_serial, purchase_date, suppress_print=False):
    """
    :usage: Allows users to create an order to enroll a unit for AppleCare (APP/AC+). It is recommended that this API
            always be preceded by a verifyOrder API call, to increase the chances of a successful order creation.
    :param invoice_number: Invoice number from POS
    :param first_name: Customer's first name as shown on invoice
    :param last_name: Customer's last name as shown on invoice
    :param company_name: Customer's company as shown on invoice (optional)
    :param email_address: Customer's email address as shown on invoice
    :param address_line1: First line of Customer's street address as shown on invoice (optional)
    :param address_line2: Second line of Customer's street address as shown on invoice (optional)
    :param city: City of Customer's street address as shown on invoice (optional)
    :param state: State of Customer's street address as shown on invoice (optional)
    :param zip_code: Zip Code of Customer's street address as shown on invoice (optional)
    :param device_id: Serial number of the AppleCare eligible device sold
    :param secondary_serial: Serial number the secondary AppleCare eligible device sold (Thunderbolt Display, optional)
    :param purchase_date: Purchase date of the AppleCare eligible device
    :param suppress_print: Suppress any print output from function (Default: False)
    :return: JSON formatted strings of the complete API request, response, and any error codes
    """
    # Establish request variables
    session, acc_ship_to, base_url = acc_credentials()

    post_url = '{0}/create-order/'.format(str(base_url))
    call_type = 'create_order'

    # Create request array
    request_array = dict(shipTo=acc_ship_to, timeZone="420", langCode="en")

    # Customer Request array
    customer = dict(
        customerEmailId=email_address, address_line1=address_line1, address_line2=address_line2, city=city,
        stateCode=state, countryCode="US", zipCode=zip_code
    )
    # Use 'company_name' if 'first_name' and 'last_name' combined is longer than 34 characters
    full_name = '{0} {1}'.format(str(first_name), str(last_name))
    if len(full_name) > 34:
        customer['company_name'] = full_name
        customer['customerFirstName'] = ""
        customer['customerLastName'] = ""
    else:
        customer['company_name'] = company_name
        customer['customerFirstName'] = first_name
        customer['customerLastName'] = last_name

    # deviceRequest
    device = dict(
        deviceId=device_id.upper(), secondarySerialNumber=secondary_serial,
        hardwareDateOfPurchase=purchase_date, verifyMPN="", nsPart=""
    )

    # Prepare data in array
    post_data = dict(
        requestContext=request_array, customerRequest=customer, deviceRequest=device,
        appleCareSalesDate=purchase_date, pocLanguage="ENG", pocDeliveryPreference="E",
        purchaseOrderNumber=invoice_number, marketID="", overridePocFlag="", emailFlag="1"
    )

    # Format post_data as JSON
    full_request = json.dumps(post_data)

    # Send data to API
    response = session.post(post_url, data=full_request)

    # Call return handler function to parse request response
    full_response, error_code, error_message = response_handler(response.text, suppress_print)

    return post_data, full_response, error_code, error_message, call_type


def cancel_order(device_id, cancellation_date, cancel_reason_code, suppress_print=False):
    """
    :usage: Designed to cancel an Auto Enrollment (AE) Order for AppleCare (APP/AC+).
    :param device_id: Serial number of the AppleCare eligible device sold
    :param cancellation_date: Date the device and AppleCare were refunded as shown on the return invoice
    :param cancel_reason_code: Cancellation code explaing why device was returned
    :param suppress_print: Suppress any print output from function (Default: False)
    :return: JSON formatted strings of the complete API request, response, and any error codes
    """
    # Establish request variables
    session, acc_ship_to, base_url = acc_credentials()

    post_url = '{0}/cancel-order/'.format(str(base_url))
    call_type = 'cancel_order'

    # Create request array
    request_array = dict(shipTo=acc_ship_to, timeZone="420", langCode="en")

    # Prepare data in array
    post_data = dict(
        requestContext=request_array, deviceId=device_id.upper(), cancellationDate=cancellation_date,
        purchaseOrderNumber="", cancelReasonCode=cancel_reason_code
    )

    # Format post_data as JSON
    full_request = json.dumps(post_data)

    # Send data to API
    response = session.post(post_url, data=full_request)

    # Call return handler function to parse request response
    full_response, error_code, error_message = response_handler(response.text, suppress_print)

    return post_data, full_response, error_code, error_message, call_type


def three_sixty_lookup(invoice_number, device_id, email_address, suppress_print=False):
    """
    :usage: Designed to search a details of the device based on various parameters.
    :param invoice_number: Refund invoice number from POS
    :param device_id: Serial number of the AppleCare eligible device sold
    :param email_address: Registered email associated with AppleCare Enrollment
    :param suppress_print: Suppress any print output from function (Default: False)
    :return: JSON formatted strings of the complete API request, response, and any error codes
    """
    # Establish request variables
    session, acc_ship_to, base_url = acc_credentials()

    post_url = '{0}/get-order/'.format(str(base_url))
    call_type = 'three_sixty_lookup'

    # Create request array
    request_array = dict(shipTo=acc_ship_to, timeZone="420", langCode="en")

    # Prepare data in array
    post_data = dict(requestContext=request_array)

    # Only one variable is needed. Only pass the one we get.
    if device_id:
        post_data['deviceId'] = device_id.upper()
        post_data['purchaseOrderNumber'] = ""
        post_data['customerEmailId'] = ""
    elif not device_id and invoice_number:
        post_data['purchaseOrderNumber'] = invoice_number
        post_data['deviceId'] = ""
        post_data['customerEmailId'] = ""
    elif not device_id and not invoice_number and email_address:
        post_data['customerEmailId'] = email_address
        post_data['deviceId'] = ""
        post_data['purchaseOrderNumber'] = ""

    # Prepare the post_data for the API
    full_request = json.dumps(post_data)

    # Send data to API
    response = session.post(post_url, data=full_request)

    # Call return handler function to parse request response
    full_response, error_code, error_message = response_handler(response.text, suppress_print)

    return post_data, full_response, error_code, error_message, call_type
