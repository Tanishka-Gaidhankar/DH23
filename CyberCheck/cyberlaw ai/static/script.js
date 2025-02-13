const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const loading = document.getElementById('loading');

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle FAQ clicks
document.querySelectorAll('.faq-list li').forEach(faq => {
    faq.addEventListener('click', function() {
        userInput.value = this.textContent;
        handleSubmit();
    });
});

// Handle form submission
async function handleSubmit() {
    const question = userInput.value.trim();
    if (!question) return;

    // Disable input and button while processing
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message
    addMessage('You', question, 'user-message');
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Show loading indicator
    loading.style.display = 'block';
    
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();

        if (response.ok) {
            // Add assistant message with formatted answer
            addMessage('Cyber Law Assistant', data.formatted_answer, 'assistant-message');
        } else {
            // Add error message
            addMessage('Error', data.error, 'assistant-message');
        }
    } catch (error) {
        addMessage('Error', 'Sorry, something went wrong. Please try again.', 'assistant-message');
    } finally {
        // Hide loading indicator and re-enable input
        loading.style.display = 'none';
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

function addMessage(sender, content, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const header = document.createElement('div');
    header.className = 'message-header';
    header.textContent = sender;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = content;
    
    messageDiv.appendChild(header);
    messageDiv.appendChild(messageContent);
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Event listeners
sendButton.addEventListener('click', handleSubmit);

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
    }
});

// Focus input on page load
userInput.focus();