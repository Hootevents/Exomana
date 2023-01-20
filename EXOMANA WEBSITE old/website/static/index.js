// Schickt einen Post request an die deleteNote funktion mit der entsprechenden Noteid
// Nach der Antwort refreshed die Seite
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
