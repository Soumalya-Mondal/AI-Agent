// Get DOM elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

// Token tracking DOM elements
const inputTokenCount = document.getElementById('inputTokenCount');
const outputTokenCount = document.getElementById('outputTokenCount');
const totalTokenCount = document.getElementById('totalTokenCount');

// Token tracking variables
let cumulativeInputTokens = 0;
let cumulativeOutputTokens = 0;

// Send message on button click
sendBtn.addEventListener('click', sendMessage);

// Send message on Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

/**
 * Send user message to the backend and display response
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Disable input and button while processing
    userInput.disabled = true;
    sendBtn.disabled = true;
    
    // Display user message
    displayMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send message to backend API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        if (response.ok) {
            // Display assistant response
            displayMessage(data.response, 'assistant');
            
            // Update token counts if available
            if (data.input_tokens !== undefined && data.output_tokens !== undefined) {
                updateTokenCounts(data.input_tokens, data.output_tokens);
            }
        } else {
            // Display error message
            displayMessage(
                `Error: ${data.error || 'Failed to get response from the assistant'}`,
                'assistant'
            );
        }
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        displayMessage(
            'Error: Unable to connect to the server. Please make sure the backend is running.',
            'assistant'
        );
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

/**
 * Update cumulative token counts and display in sidebar
 * @param {number} inputTokens - Input tokens from this response
 * @param {number} outputTokens - Output tokens from this response
 */
function updateTokenCounts(inputTokens, outputTokens) {
    // Add to cumulative counts
    cumulativeInputTokens += inputTokens;
    cumulativeOutputTokens += outputTokens;
    
    // Update DOM elements
    inputTokenCount.textContent = cumulativeInputTokens;
    outputTokenCount.textContent = cumulativeOutputTokens;
    totalTokenCount.textContent = cumulativeInputTokens + cumulativeOutputTokens;
    
    // Add visual feedback (optional)
    flashElement(inputTokenCount);
    flashElement(outputTokenCount);
    flashElement(totalTokenCount);
}

/**
 * Flash element to indicate update
 * @param {Element} element - DOM element to flash
 */
function flashElement(element) {
    element.style.animation = 'none';
    setTimeout(() => {
        element.style.animation = 'pulse 0.5s ease-in-out';
    }, 10);
}
function displayMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.class = `message ${sender}-message`;
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to the latest message
    scrollToBottom();
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

/**
 * Scroll chat messages to the bottom
 */
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 0);
}

// Set focus on input when page loads
window.addEventListener('load', () => {
    userInput.focus();
});
