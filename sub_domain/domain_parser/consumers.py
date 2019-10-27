import json
import aiodns
import itertools
from aiodns.error import DNSError

from domain_parser.subdomains import most_popular_subdomains

from channels.consumer import AsyncConsumer

CHUNK_LEN = 1

dom = ''

def deep_check(deep):
    if 1 <= deep <= 3:
        return deep
    else:
        return 1

def count_domains(deep):
    return sum([len(most_popular_subdomains)**i for i in range(1, deep+1)])

def domains_chunks(domain, deep = 1):
    for repeat_i in range(1, deep+1):
        subdomains_combos = itertools.product(most_popular_subdomains, repeat=deep)
        combos_len = len(most_popular_subdomains)**repeat_i
        for chunk_i in range(combos_len // CHUNK_LEN):
            chunk = set()
            for _ in range(chunk_i * CHUNK_LEN, min((chunk_i + 1) * CHUNK_LEN, combos_len)):
                full_domain = '.'.join(next(subdomains_combos))
                chunk.add(f'{full_domain}.{domain}')
            yield chunk

async def check_domain(domain, dns_resolver):
    global dom
    try: 
        await dns_resolver.query(domain, 'A')
        dom = domain
    except (DNSError, UnicodeError):
        dom = 'Bad!'
    return dom

async def re_print_data(class_, data):
        new_data = {
            'data': data
        }
        await class_.send({
            'type': 'websocket.send',
            'text': json.dumps(new_data)
        })

class DataConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connection successful', event)
        await self.send({
            'type': 'websocket.accept'
        })

        
    async def websocket_receive(self, event):
        data = json.loads(event.get('text'))
        domain = data.get('domain')
        deep = deep_check(int(data.get('deep')))
        dns_resolver = aiodns.DNSResolver() 
        global dom
        for chunk in domains_chunks(domain, deep):
            chunk = list(chunk)[0]
            await check_domain(chunk, dns_resolver)
            if dom != 'Bad!':
                await re_print_data(self, dom)
        print('Done!')
    



  








##############################################################
# Это работает!!!

# import json
# import aiodns
# from aiodns.error import DNSError

# from domain_parser.subdomains import most_popular_subdomains

# import json

# from channels.consumer import AsyncConsumer

# dom = ''

# def deep_check(deep):
#     if 1 <= deep <= 3:
#         return deep
#     else:
#         return 1

# def count_domains(deep):
#     return sum([len(most_popular_subdomains)**i for i in range(1, deep+1)])

# def domains_chunks(domain, deep = 1):
#     for repeat_i in range(1, deep+1):
#         subdomains_combos = itertools.product(most_popular_subdomains, repeat=deep)
#         combos_len = len(most_popular_subdomains)**repeat_i
#         for chunk_i in range(combos_len // CHUNK_LEN):
#             chunk = set()
#             for _ in range(chunk_i * CHUNK_LEN, min((chunk_i + 1) * CHUNK_LEN, combos_len)):
#                 full_domain = '.'.join(next(subdomains_combos))
#                 chunk.add(check_domain(f'{full_domain}.{domain}'))
#             yield chunk

# async def check_domain(domain, dns_resolver):
#     print('check')
#     global dom
#     try: 
#         await dns_resolver.query(domain, 'A')
#         dom = 'Done!'
#     except (DNSError, UnicodeError):
#         dom = 'Bad!'
#     return dom

# async def re_print_data(class_, data):
#         new_data = {
#             'data': data
#         }
#         await class_.send({
#             'type': 'websocket.send',
#             'text': json.dumps(new_data)
#         })

# class DataConsumer(AsyncConsumer):

#     async def websocket_connect(self, event):
#         print('connection successful', event)
#         await self.send({
#             'type': 'websocket.accept'
#         })

        
#     async def websocket_receive(self, event):
#         data = json.loads(event.get('text'))
#         domain = data.get('domain')
#         deep = deep_check(int(data.get('deep')))
#         dns_resolver = aiodns.DNSResolver() 
#         global dom
#         await check_domain(domain, dns_resolver)
#         print(dom)
#         await re_print_data(self, dom)