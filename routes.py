import collaborators
import labels
import notes
import user

all_routes = user.api_routes + notes.notes_routes + labels.label_routes + collaborators.collaborators_routes
