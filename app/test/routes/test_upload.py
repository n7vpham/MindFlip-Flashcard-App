from pathlib import Path
from werkzeug.datastructures import FileStorage

resources = Path(__file__).parent.parent / "resources"

def test_upload(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["user_id"] = 1

    with open(resources / "testmd.md", "rb") as file:
        file_storage = FileStorage(stream=file, filename="testmd.md", content_type="text/markdown")

        response = client.post(
            "/flashcards/upload",
            data={
                "setName": "test",
                "setDescription": "A test set description",
                "file": file_storage  # Simulating file upload
            },
        )

    print(response.data)
    assert response.status_code == 200
    
