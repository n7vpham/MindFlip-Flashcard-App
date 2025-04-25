// edit.js

function deleteFlashcard(front) {
    const data = {card_front: front};

    fetch(`/flashcards/${set_id}/api/delete`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => {
        if (res.ok) {
            // Optionally refresh page or remove element from DOM
            location.reload();
        } else {
            res.json().then(data => alert(data.error || "Failed to delete flashcard."));
        }
    })
    .catch(err => {
        console.error("Error deleting flashcard:", err);
    });
    
}

function renderFlashcards(filteredCards = flashcards) {
    const container = document.getElementById('flashcardContainer');
    container.innerHTML = '';
    let index = 0;
    filteredCards.forEach(card => {
        const div = document.createElement('div');
        div.className = 'flashcard';
        div.dataset.id = index;
        div.innerHTML = `
            <div class="flashcard-content">
                <p class="fl-front"><strong>Front:</strong> ${card.front}</p>
                <p class="fl-back"><strong>Back:</strong> ${card.back}</p>
            </div>
            <div class="flashcard-actions">
                <button class="btn-action btn-edit">Edit</button>
                <button class="btn-action btn-delete" onclick="deleteFlashcards()">Delete</button>
            </div>
        `;

        div.querySelector('.btn-edit').addEventListener('click', () => {
            editFlashcard(card.front, card.back);
        });

        div.querySelector('.btn-delete').addEventListener('click', () => {
            deleteFlashcard(card.front);
        });

        container.appendChild(div);
        index++;
    });
}

window.onload = () => {
    renderFlashcards(flashcards)
}
