from microservice_request.services import MicroServiceConnect


class BlogMicroService(MicroServiceConnect):
    lookup_prefix = '/chat'
    api_key = '3sgyqgmW.SftRAyxMLuuJdulTqrewFGUYLmqnWUJh'
    service = 'http://web:8000'
