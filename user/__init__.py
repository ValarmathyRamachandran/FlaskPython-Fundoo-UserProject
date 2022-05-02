from labels import AddLabel
from labels.apis import DeleteLabel
from notes import CreateNotes, GetNotes
from notes.apis import UpdateNote, DeleteNote, GetTrash, GetArchived, NoteOperations, GetPinned
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
    ('/gettrash', GetTrash),
    ('/noteoperation', NoteOperations),
    ('/getpinned', GetPinned),
    ('/getarchived', GetArchived),
    ('/addlabel', AddLabel),
    ('/deletelabel', DeleteLabel)

]
