from user.apis import Registration, Login, AccountActivation, ForgotPassword, ResetPassword

api_routes = [
    (Registration, '/registration'),
    (Login, '/login'),
    (AccountActivation, '/activation'),
    (ForgotPassword, '/forgotpassword'),
    (ResetPassword, '/resetpassword'),
    # ('/createnote', CreateNotes),
    # ('/getnotes', GetNotes),
    # ('/updatenote', UpdateNote),
    # ('/deletenote', DeleteNote),
    # ('/gettrash', GetTrash),
    # ('/noteoperation', NoteOperations),
    # ('/getpinned', GetPinned),
    # ('/getarchived', GetArchived),
    # ('/addlabel', AddLabel),
    # ('/deletelabel', DeleteLabel),
    # ('/addcollabortors', AddCollaborators),
    # ('/label', NoteLabel),
    # ('/notecollabortors', NoteCollaborators)
]
