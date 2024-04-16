class PaymentHandler:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def process_payment(self, payment, amount):
        """
        Process a payment through the payment gateway.
        :param payment: The Payment object representing the payment.
        :param amount: The amount of the payment.
        :return: The result of the payment processing.
        """
        # Code to communicate with the payment gateway API and process the payment goes here
        result = {'success': True, 'message': 'Payment processed successfully.'}
        return result

    def refund_payment(self, payment, amount):
        """
        Refund a payment through the payment gateway.
        :param payment: The Payment object representing the payment.
        :param amount: The amount of the refund.
        :return: The result of the refund processing.
        """
        # Code to communicate with the payment gateway API and process the refund goes here
        result = {'success': True, 'message': 'Refund processed successfully.'}
        return result


