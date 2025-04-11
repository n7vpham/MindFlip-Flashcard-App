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

// Flashcard Management
let flashcards = [
    { id: 1, question: "What is the capital of France?", answer: "Paris" },
    { id: 2, question: "What is 2 + 2?", answer: "4" },
    { id: 3, question: "Who wrote Romeo and Juliet?", answer: "Shakespeare" }
];

function renderFlashcards(filteredCards = flashcards) {
    const container = document.getElementById('flashcardContainer');
    container.innerHTML = '';
    filteredCards.forEach(card => {
        const div = document.createElement('div');
        div.className = 'flashcard';
        div.dataset.id = card.id;
        div.innerHTML = `
            <div class="flashcard-content">
                <p><strong>Q:</strong> ${card.question}</p>
                <p><strong>A:</strong> ${card.answer}</p>
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

function deleteFlashcard(id) {
    flashcards = flashcards.filter(f => f.id !== id);
    renderFlashcards();
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