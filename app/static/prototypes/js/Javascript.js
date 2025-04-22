// Particle Background
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particlesArray = [];
const numberOfParticles = 50;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 5 + 1;
        this.speedX = Math.random() * 1 - 0.5;
        this.speedY = Math.random() * 1 - 0.5;
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.size > 0.2) this.size -= 0.01;
    }
    draw() {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function init() {
    for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();
        if (particlesArray[i].size <= 0.2) {
            particlesArray.splice(i, 1);
            i--;
            particlesArray.push(new Particle());
        }
    }
    requestAnimationFrame(animate);
}

init();
animate();

/*
// Flashcard Management
let flashcards = [
    { id: 1, question: "What is the capital of France?", answer: "Paris" },
    { id: 2, question: "What is 2 + 2?", answer: "4" },
    { id: 3, question: "Who wrote Romeo and Juliet?", answer: "Shakespeare" }
];
*/

let flashcards = [];

function renderFlashcards(filteredCards = flashcards) {
    const container = document.getElementById('flashcardContainer');
    container.innerHTML = '';
    filteredCards.forEach(card => {
        const div = document.createElement('div');
        div.className = 'flashcard';
        div.dataset.id = card.id;
        div.innerHTML = `
            <div class="flashcard-content">
                <p><strong>Front:</strong> ${card.question}</p>
                <p><strong>Back:</strong> ${card.answer}</p>
            </div>
            <div class="flashcard-actions">
                <button class="btn-action" onclick="editFlashcard(${card.id})">Edit</button>
                <button class="btn-action btn-delete" onclick="deleteFlashcard(${card.id})">Delete</button>
            </div>
        `;
        container.appendChild(div);
    });
}

function createFlashcard() {
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
    if (question && answer) {
        const newId = flashcards.length ? Math.max(...flashcards.map(f => f.id)) + 1 : 1;
        flashcards.push({ id: newId, question, answer });
        renderFlashcards();
        document.getElementById('createForm').reset();
        bootstrap.Modal.getInstance(document.getElementById('createModal')).hide();
    }
}

function editFlashcard(id) {
    const card = flashcards.find(f => f.id === id);
    if (card) {
        document.getElementById('editId').value = id;
        document.getElementById('editQuestion').value = card.question;
        document.getElementById('editAnswer').value = card.answer;
        new bootstrap.Modal(document.getElementById('editModal')).show();
    }
}

function saveEdit() {
    const id = parseInt(document.getElementById('editId').value);
    const question = document.getElementById('editQuestion').value;
    const answer = document.getElementById('editAnswer').value;
    if (question && answer) {
        const cardIndex = flashcards.findIndex(f => f.id === id);
        flashcards[cardIndex] = { id, question, answer };
        renderFlashcards();
        bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
    }
}

function deleteSet(setID) {
    fetch(`/flashcards/${setID}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if (res.ok) {
            // Optionally refresh page or remove element from DOM
            location.reload();
        } else {
            res.json().then(data => alert(data.error || "Failed to delete set."));
        }
    })
    .catch(err => {
        console.error("Error deleting set:", err);
    });
}

function searchFlashcards() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filterType = document.getElementById('filterSelect').value;

    let filteredCards = flashcards;
    if (searchTerm) {
        if (filterType === 'question') {
            filteredCards = flashcards.filter(card => card.question.toLowerCase().includes(searchTerm));
        } else if (filterType === 'answer') {
            filteredCards = flashcards.filter(card => card.answer.toLowerCase().includes(searchTerm));
        } else {
            filteredCards = flashcards.filter(card => 
                card.question.toLowerCase().includes(searchTerm) || 
                card.answer.toLowerCase().includes(searchTerm)
            );
        }
    }
    renderFlashcards(filteredCards);
}

// Initial render
renderFlashcards();

// Search on Enter key
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchFlashcards();
    }
});
function showSignup() {
    const card = document.getElementById('card');
    card.classList.add('signup');
}

function showLogin() {
    const card = document.getElementById('card');
    card.classList.remove('signup');
}
function showQuestion() {
    const card = document.getElementById('card');
    if (card.classList.contains('answer')) {
        card.classList.remove('answer');
    }
}

function showAnswer() {
    const card = document.getElementById('card');
    card.classList.add('answer');
}
function addRow() {
    const container = document.getElementById('bulkEntries');
    const row = document.createElement('div');
    row.className = 'bulk-entry-row row g-3 mb-3';
    row.innerHTML = `
        <div class="col-md-6">
            <textarea class="form-control question-input" name="front" placeholder="Front" rows="3" required></textarea>
        </div>
        <div class="col-md-6">
            <textarea class="form-control answer-input" name="back" placeholder="Back" rows="3" required></textarea>
        </div>
        <div class="col-md-+">
            <button type="button" class="btn btn-delete w-100" onclick="removeRow(this)">Remove</button>
        </div>
    `;
    container.appendChild(row);
}

function removeRow(button) {
    const rows = document.querySelectorAll('.bulk-entry-row');
    if (rows.length > 1) {
        button.closest('.bulk-entry-row').remove();
    } else {
        alert('At least one row is required.');
    }
}


function createBulkFlashcards() {
    const inputs = document.querySelectorAll('.bulk-entry-row');
    let validEntries = 0;
    let newFlashcards = [];

    inputs.forEach(row => {
        const question = row.querySelector('.question-input').value.trim();
        const answer = row.querySelector('.answer-input').value.trim();
        if (question && answer) {
            const newId = flashcards.length ? Math.max(...flashcards.map(f => f.id)) + 1 + validEntries : 1 + validEntries;
            newFlashcards.push({ id: newId, question, answer });
            validEntries++;
        }
    });

    if (validEntries > 0) {
        flashcards.push(...newFlashcards);
        alert(`${validEntries} flashcard(s) added successfully!`);
        renderFlashcards();
        document.getElementById('bulkForm').reset();
        const container = document.getElementById('bulkEntries');
        container.innerHTML = `
            <div class="bulk-entry-row row g-3 mb-3">
                <div class="col-md-6">
                    <textarea class="form-control question-input" placeholder="Enter Front" rows="3" required></textarea>
                </div>
                <div class="col-md-6">
                    <textarea class="form-control answer-input" placeholder="Enter Back" rows="3" required></textarea>
                </div>
                <div class="col-md-+">
                    <button type="button" class="btn btn-delete w-100" onclick="removeRow(this)">Remove</button>
                </div>
            </div>
        `;
    } else {
        alert('Please fill in at least one valid question-answer pair.');
    }
}

function showManualForm() {
    document.getElementById('manualForm').style.display = 'block';
    document.getElementById('uploadForm').style.display = 'none';
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('button[onclick="showManualForm()"]').classList.add('active');
}

function showUploadForm() {
    document.getElementById('manualForm').style.display = 'none';
    document.getElementById('uploadForm').style.display = 'block';
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('button[onclick="showUploadForm()"]').classList.add('active');
}

function openSet(){
    window.location.href = "flashcard_set.html";

}

function editSet(){
    window.location.href = "manage_flashcards.html";

}




/*
function renderCard(index) {
    const card = document.getElementById('card');
    card.innerHTML = `
    <div class="question-form" onclick="showAnswer()">
        <h3>${flashcards[index].question}</h3>
    </div>
    <div class="answer-form" onclick="showQuestion()">
        <h3>${flashcards[index].answer}</h3>
    </div>
    `;
  showQuestion(); // Start with question side visible
}

function nextCard() {
    currentIndex = (currentIndex + 1) % flashcards.length;
    renderCard(currentIndex);
}

function prevCard() {
    currentIndex = (currentIndex - 1 + flashcards.length) % flashcards.length;
    renderCard(currentIndex);
}
// Initialize the first card when the page loads
window.onload = () => {
    renderCard(currentIndex);
};
*/
