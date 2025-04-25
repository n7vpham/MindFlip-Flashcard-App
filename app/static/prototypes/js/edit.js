// edit.js

function renderFlashcards(filteredCards = flashcards) {
    const container = document.getElementById('flashcardContainer');
    container.innerHTML = '';
    filteredCards.forEach(card => {
        const div = document.createElement('div');
        div.className = 'flashcard';
        div.dataset.id = card.id;
        div.innerHTML = `
            <div class="flashcard-content">
                <p><strong>Front:</strong> ${card.front}</p>
                <p><strong>Back:</strong> ${card.back}</p>
            </div>
            <div class="flashcard-actions">
                <button class="btn-action" onclick="editFlashcard(${card.id})">Edit</button>
                <button class="btn-action btn-delete" onclick="deleteFlashcard(${card.id})">Delete</button>
            </div>
        `;
        container.appendChild(div);
    });
}

window.onload = () => {
    console.log(flashcards)
    renderFlashcards(flashcards)
}
