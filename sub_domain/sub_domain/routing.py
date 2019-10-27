from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from domain_parser.consumers import DataConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        URLRouter([
            url('', DataConsumer)
        ])
    )
})