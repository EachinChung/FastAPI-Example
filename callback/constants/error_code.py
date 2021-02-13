class ErrorNode:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def unpack(self):
        return self.code, self.msg


class Error:
    timeout_error = ErrorNode("4000", "请求第三方超时")
    request_error = ErrorNode("4000", "请求第三方错误")
    inter_error = ErrorNode("5000", "系统内部错误")
    unauthorized_error = ErrorNode("4010", "请登录您的账号")
    secret_key_error = ErrorNode("4011", "密钥不存在或错误")
    forbidden_error = ErrorNode("4030", "您没有权限")
