from notes.apis import CreateNotes, GetNotes, UpdateNote, DeleteNote, GetTrash

api_routes = [
    ('/createnote', CreateNotes),
    ('/getnotes', GetNotes),
    ('/updatenote', UpdateNote),
    ('/deletenote', DeleteNote),
    ('/gettrash', GetTrash)
]
