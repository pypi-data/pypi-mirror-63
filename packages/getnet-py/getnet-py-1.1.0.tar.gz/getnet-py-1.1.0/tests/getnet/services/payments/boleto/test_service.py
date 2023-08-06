import unittest
from unittest.mock import patch

from getnet.services.customers import Customer
from getnet.services.payments import Order
from getnet.services.payments.boleto import Boleto, Service
from getnet.services.payments.payment_response import PaymentResponse
from tests.getnet.services.customers.test_customer import sample as customer_sample
from tests.getnet.services.payments.boleto.test_boleto import sample as boleto_sample
from tests.getnet.services.payments.test_payment_response import (
    sample_boleto as payment_sample,
)


@patch("getnet.Client")
class ServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.order = Order("6d2e4380-d8a3-4ccb-9138-c289182818a3", 0, "physical_goods")
        self.customer = Customer(**customer_sample.copy())

    def testCreate(self, client_mock):
        client_mock.base_url = "http://sample.org/"
        client_mock.post.return_value = payment_sample.copy()

        service = Service(client_mock)
        obj = service.create(
            amount=100,
            currency="BRL",
            order=self.order,
            boleto=Boleto(**boleto_sample),
            customer=self.customer,
        )

        self.assertIsInstance(obj, PaymentResponse)
        self.assertEqual(payment_sample.get("payment_id"), str(obj.payment_id))


if __name__ == "__main__":
    unittest.main()
