from notes.apis import CreateNotes, GetNotes, UpdateNote, DeleteNote, GetTrash, NoteOperations, \
    GetPinned, GetArchived, NoteLabel

notes_routes = [
    (CreateNotes, '/createnote'),
    (GetNotes, '/getnotes'),
    (UpdateNote, '/updatenote'),
    (DeleteNote, '/deletenote'),
    (GetTrash, '/gettrash'),
    (NoteOperations, '/noteoperation'),
    (GetPinned, '/getpinned'),
    (GetArchived, '/getarchived'),
    (NoteLabel, '/label')

]
