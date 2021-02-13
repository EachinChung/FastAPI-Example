from fastapi import Request


def get_client_ip(request: Request) -> str:
    """获取客户端的ip

    Args:
        request (Request)

    Returns:
        str: ip
    """
    if x_forwarded_for := request.headers.getlist('X-Forwarded-For'):
        return x_forwarded_for[0]

    if x_real_ip := request.headers.get('X-Real-IP'):
        return x_real_ip

    return request.client.host
