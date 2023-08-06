## GWX Payment
Payment gateway integration bridge for python, specifically flask based applications.

### Dependencies
- Python 3.7^
- PyYAML
- stripe
- Werkzeug 0.16^

### Installation
1. Install the package using pip, by executing:
```python
pip install -U gwx-payment
```

2. Create the `<your_config_name>.yaml` file, this MUST follow the following convention:

```yaml


 
# This indicates the current `Active` payment service 
provider: stripe


stripe:
  api_url: <api_url>
  public_key: <public_key>
  api_key: <api_key>
  success_url: <success_url>
  cancel_url: <cancel_url>

paypal:
  api_url: <api_url>
  public_key: <public_key>
  api_key: <api_key>
  success_url: <success_url>
  cancel_url: <cancel_url>
```


### Quickstart
First import the Provider Service class

```python
from gwx_payment.provider_service import ProviderService
``` 

Then instantiate the ProviderService class along with it's config dependencies:

```python
payment_variable = ProviderService('/path/to/config/dir', 'your_config_name.yaml').get_payment_service()
```

The provider service accepts a `.yaml` file type as it's config file.
Viola! you can now use it for your payment transactions.

### Usage
The following are the methods available within the AbstractPaymentService and their functionality.


| Method Name                            | Functionality                                                              
| -------------------------------------- | ---------------------------------------------------------------------
|                                        |
| **create_payment**                     | Checkout method, this will initiate the payment transaction.
|                                        | :param kwargs: the parameters for the payment creation.
|                                        | :return: structured value required for response composition.
|                                        |
| **get_payment**                        | Retrieve a specific payment record
|                                        | :param payment_id: the primary id used to reference against an endpoint.
|                                        | :return: the retrieved record, null if none found.
|                                        |
| **confirm_payment**                    | Confirm the payment, this states that the payment has been accepted,
|                                        | and sent to the vendor.
|                                        | :param kwargs: named payload parameters
|                                        | :return: structured value required for response composition.

