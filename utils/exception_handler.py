import logging

from rest_framework.views import exception_handler

logger = logging.getLogger("apps")


def custom_exception_handler(exc, context):
    # 先讓 DRF 處理標準的回應
    response = exception_handler(exc, context)

    # 如果有回應則記錄詳細的錯誤資訊
    if response is not None:
        request = context.get("request")

        # 取得 IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = (
            x_forwarded_for.split(",")[0]
            if x_forwarded_for
            else request.META.get("REMOTE_ADDR")
        )

        # 取得 User
        user = request.user if request.user else "Anonymous"

        # 取得請求路徑與方法
        path = request.path
        method = request.method

        # 寫入 Log
        logger.error(
            f"API Error | Status: {response.status_code} | User: {user} | IP: {ip} | "
            f"Method: {method} | Path: {path} | Detail: {response.data}"
        )

    return response
