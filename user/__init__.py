from collaborators.apis import AddCollaborators
from labels import AddLabel, DeleteLabel

from notes import CreateNotes, GetNotes
from notes.apis import UpdateNote, DeleteNote, GetTrash, GetArchived, NoteOperations, GetPinned, NoteLabel, \
    NoteCollaborators
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
    ('/deletelabel', DeleteLabel),
    ('/addcollabortors', AddCollaborators),
    ('/label', NoteLabel),
    ('/notecollabortors', NoteCollaborators)
]
