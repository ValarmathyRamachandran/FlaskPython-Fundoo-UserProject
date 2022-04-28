from notes import CreateNotes, GetNotes
from notes.apis import UpdateNote, DeleteNote, GetTrash, GetPinned, ArchiveNote, GetArchived, PinnedNote
from user.apis import Registration, Login, AccountActivation, ForgotPassword, ResetPassword

api_routes = [
    ('/registration', Registration),
    ('/login', Login),
    ('/activation', AccountActivation),
    ('/forgotpassword', ForgotPassword),
    ('/resetpassword', ResetPassword),
    ('/createnote', CreateNotes),
    ('/getnotes', GetNotes),
    ('/updatenote', UpdateNote),
    ('/deletenote', DeleteNote),
    ('/pinnednote', PinnedNote),
    ('/gettrash', GetTrash),
    ('/getpinned', GetPinned),
    ('/archivenote', ArchiveNote),
    ('/getarchived', GetArchived)

]
