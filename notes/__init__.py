from notes.apis import CreateNotes, GetNotes, UpdateNote, DeleteNote

api_routes = [
    ('/createnote', CreateNotes),
    ('/getnotes', GetNotes),
    ('/updatenote', UpdateNote),
    ('/deletenote', DeleteNote)
]
