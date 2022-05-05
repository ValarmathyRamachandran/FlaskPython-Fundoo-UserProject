from .apis import AddLabel, DeleteLabel

label_routes = [
    (AddLabel, '/addlabel'),
    (DeleteLabel, '/deletelabel')
]
