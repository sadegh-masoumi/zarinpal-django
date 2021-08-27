from .zarinpal import ZarinPal
from django.http import HttpResponse


pay = ZarinPal(merchant='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', call_back_url="http://localhost:8000/verify/")


def send_request(request):
    # email and mobile is optimal
    response = pay.send_request(amount='1000', description='توضیحات مربوط به پرداخت', email="Example@test.com",
                               mobile='09123456789')
    if response.get('error_code') is None:
        # redirect object
        return response
    else:
        return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')


def verify(request):
    response = pay.verify(request=request, amount='1000')

    if response.get("transaction"):
        if response.get("pay"):
            return HttpResponse('تراکنش با موفقت انجام شد')
        else:
            return HttpResponse('این تراکنش با موفقیت انجام شده است و الان دوباره verify شده است')
    else:
        if response.get("status") == "ok":
            return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')
        elif response.get("status") == "cancel":
            return HttpResponse(f'تراکنش ناموفق بوده است یا توسط کاربر لغو شده است'
                                f'Error Message: {response.get("message")}')
