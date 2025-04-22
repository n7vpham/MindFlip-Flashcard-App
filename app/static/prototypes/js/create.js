// create.js

// because there is logic to parse markdown files on the backend, if the file is
// markdown here we simply post the form to /flashcards/upload.
// if csv or txt I just called the createBulkFlashcards() like before.
function uploadFile() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file.');
        return false;
    }

    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.md')) {
        console.log('Markdown file is valid.');
        form.action = '/flashcards/upload';
        console.log(form.action, form.method, form.enctype);
        form.submit();
        return true;
    } else if (fileName.endsWith('.csv') || fileName.endsWith('.txt')) {
        console.log(`Creating flashcards from ${fileName}`)
        createBulkFlashcards();
    } else {
        alert('Unsupported file type.');
        return false;
    }
};

