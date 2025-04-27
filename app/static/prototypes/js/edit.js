// edit.js
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    const clearButton = document.getElementById('clearButton');

    searchInput.addEventListener('input', filterFlashcards);
    filterSelect.addEventListener('change', filterFlashcards);
    clearButton.addEventListener('click', function () {
        searchInput.value = '';
        filterFlashcards();
    });
});

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
                <button class="btn-action btn-delete">Delete</button>
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

let fadeTimers = new Map();

function filterFlashcards() {
    const searchInput = document.getElementById('searchInput').value.trim().toLowerCase();
    const filterType = document.getElementById('filterSelect').value;
    const flashcardDivs = document.querySelectorAll('.flashcard');

    flashcardDivs.forEach(div => {
        const front = div.querySelector('.fl-front')?.textContent.split(':')[1]?.trim().toLowerCase() || '';
        const back = div.querySelector('.fl-back')?.textContent.split(':')[1]?.trim().toLowerCase() || '';

        let isVisible = false;
        if (filterType === 'all') {
            isVisible = front.includes(searchInput) || back.includes(searchInput);
        } else if (filterType === 'front') {
            isVisible = front.includes(searchInput);
        } else if (filterType === 'back') {
            isVisible = back.includes(searchInput);
        }

        if (searchInput === '' || isVisible) {
            if (fadeTimers.has(div)) {
                clearTimeout(fadeTimers.get(div));
                fadeTimers.delete(div);
            }
            div.style.display = 'flex';
            div.classList.remove('fade-out-card');
            div.classList.add('fade-in-card');
        } else {
            if (!div.classList.contains('fade-out-card')) {
                div.classList.remove('fade-in-card');
                div.classList.add('fade-out-card');

                const timer = setTimeout(() => {
                    div.style.display = 'none';
                    div.classList.add('hidden-card');
                    fadeTimers.delete(div);
                }, 500);

                fadeTimers.set(div, timer);
            }
        }
    });
}

window.onload = () => {
    renderFlashcards(flashcards)
}
