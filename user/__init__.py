from user.apis import Registration, Login, AccountActivation, ForgotPassword, ResetPassword, GetAllUsers

api_routes = [
    (Registration, '/registration'),
    (Login, '/login'),
    (AccountActivation, '/activation'),
    (ForgotPassword, '/forgotpassword'),
    (ResetPassword, '/resetpassword'),
    (GetAllUsers, '/getallusers')

]


