from flask import views

from notes.apis import CreateNotes, GetNotes, UpdateNote, DeleteNote, GetTrash, NoteOperations, GetPinned, GetArchived, \
    NoteLabel

notes_routes = [
    ('/createnote', CreateNotes),
    ('/getnotes', GetNotes),
    ('/updatenote', UpdateNote),
    ('/deletenote', DeleteNote),
    ('/gettrash', GetTrash),
    ('/noteoperation', NoteOperations),
    ('/getpinned', GetPinned),
    ('/getarchived', GetArchived),
    ('/label', NoteLabel)

]
