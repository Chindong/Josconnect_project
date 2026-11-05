import hashlib
import hmac
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
 
@csrf_exempt
@require_POST
def paystack_webhook(request):
    signature = request.headers.get("x-paystack-signature", "")
    expected = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        request.body,
        hashlib.sha512
    ).hexdigest()
 
    if not signature or not hmac.compare_digest(expected, signature):
        return HttpResponse(status=400)
 
    try:
        event = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)
 
    # TODO: For charge.success:
    # 1. Find order by the unique reference.
    # 2. Lock the order row in transaction.atomic().
    # 3. Verify exact expected amount and currency.
    # 4. Verify provider status through the provider API as required.
    # 5. If not already processed, mark paid and create one ledger entry.
    # 6. Store webhook event ID/reference for idempotency.
    return HttpResponse(status=200)
