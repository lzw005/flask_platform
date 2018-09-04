import jwt, datetime, time
from models import Users
from settings import Config as config
import utils

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3),
                'iat': datetime.datetime.utcnow(),
                'iss': 'WUSHU ONLINE',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:string
        :return: dict|string payload|error
        """
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY, leeway=datetime.timedelta(seconds=600))
            # 取消过期时间验证
            # payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'


    def authenticate(self, email, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param email:string
        :param password:string
        :return: dict
        """
        # userInfo = Users.query.filter_by(username=username).first()
        userInfo = Users.query.filter(Users.email == email).first()
        if userInfo:
            if (Users.check_password(Users, userInfo.password, password)):
                login_time = int(time.time())
                userInfo.login_time = login_time
                Users.update(Users)
                token = self.encode_auth_token(userInfo.id, login_time)
                print(self.decode_auth_token(token.decode()))
                return utils.success_response('登陆成功',{'token':token.decode()})
            return utils.error_response('用户名或密码不正确', {'email': email})
        else:
            return utils.error_response('用户名或密码不正确', {'email': email})


    def identify(self, request):
        """
        用户鉴权
        :return: dict
        """
        auth_token = request.headers.get('Authorization',None)
        if auth_token:
            payload_or_error = self.decode_auth_token(auth_token)
            if not isinstance(payload_or_error, str):
                user = Users.get(Users, payload_or_error['data']['id'])
                if user:
                    if (user.login_time == payload_or_error['data']['login_time']):
                        return utils.success_response('请求成功',payload_or_error['data'])
                    else:
                        return utils.error_response('token已更改请重新获取', {'token':auth_token})
                else:
                    return utils.error_response("找不到该用户信息")
            else:
                return utils.error_response(payload_or_error,{'token':auth_token})
        else:
            return utils.error_response('没有提供认证token',{'token':''})

    # def identify(request):
    #     def wrapper(func):
    #         def inner_wrapper(*args, **kwargs):
    #             start = time.time()
    #             func(*args, **kwargs)
    #             stop = time.time()
    #             print('run time is %f' % (stop - start))
    #         return inner_wrapper()
    #     return wrapper
