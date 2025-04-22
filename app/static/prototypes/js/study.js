// study.js

let currentIndex;

function renderCard(index) {
    const card = document.getElementById('card');
    card.innerHTML = `
    <div class="question-form" onclick="showAnswer()">
        <h3>${studyCards[index].front}</h3>
    </div>
    <div class="answer-form" onclick="showQuestion()">
        <h3>${studyCards[index].back}</h3>
    </div>
    `;
  showQuestion(); // Start with question side visible
}

function nextCard() {
    currentIndex = (currentIndex + 1) % studyCards.length;
    renderCard(currentIndex);
}

function prevCard() {
    currentIndex = (currentIndex - 1 + studyCards.length) % studyCards.length;
    renderCard(currentIndex);
}
// Initialize the first card when the page loads
window.onload = () => {
    currentIndex = 0;
    renderCard(currentIndex);
};
