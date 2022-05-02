from notes.apis import CreateNotes, GetNotes, UpdateNote, DeleteNote, GetTrash, NoteOperations, GetPinned, GetArchived

notes_routes = [
    ('/createnote', CreateNotes),
    ('/getnotes', GetNotes),
    ('/updatenote', UpdateNote),
    ('/deletenote', DeleteNote),
    ('/gettrash', GetTrash),
    ('/noteoperation', NoteOperations),
    ('/getpinned', GetPinned),
    ('/getarchived', GetArchived)

]
