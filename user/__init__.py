
from user.apis import Registration, Login, AccountActivation

api_routes = [
    ('/registration', Registration),
    ('/login', Login),
    ('/activation', AccountActivation)
]
