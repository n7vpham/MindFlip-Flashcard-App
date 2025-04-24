from pathlib import Path
from werkzeug.datastructures import FileStorage

resources = Path(__file__).parent.parent / "resources"

def test_upload(client):

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

    print(response.json)
    assert response.status_code == 302

    #TODO test that the set is successfully uploaded into the db
    
def test_edit(client, test_user, test_flashcards):
    with client.session_transaction() as session:
        session['user_id'] = str(test_user['_id'])

    print(test_flashcards['_id'])
    set_id = test_flashcards['_id']
    response = client.put(f'/flashcards/edit/{set_id}', data={
        "setName": "modifiedSet",
        "setDesciption": "this set was edited",
        "front": "new f1",
        "back": "new b1",
        "front": "new f2",
        "back": "new b2"
    })

    assert response.status_code == 200
