// edit.js

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

        container.appendChild(div);
        index++;
    });
}

window.onload = () => {
    renderFlashcards(flashcards)
}
