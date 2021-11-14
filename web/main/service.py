from microservice_request.services import ConnectionService


class BlogMicroService(ConnectionService):
    lookup_prefix = '/chat'
    api_key = '3sgyqgmW.SftRAyxMLuuJdulTqrewFGUYLmqnWUJh'
    service = 'http://web:8000'
