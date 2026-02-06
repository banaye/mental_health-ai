// set initial timestamp

document.getElementById('initialTime').textContent = new Date().toLocaleTimeString();

function getCookie(name) {
    let cookievalue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookievalue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookievalue;
}

const csrftoken = getCookie('csrftoken');

function selectMood(mood) {
    // Note: Removed event parameter as it's not passed from HTML
    // If you want to highlight the button, consider passing 'this' or using a different approach
    sendQuickMessage(`I'm feeling ${mood}`);
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendQuickMessage(text) {
    document.getElementById('messageInput').value = text;
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (!message) return;
    input.disabled = true;

    document.getElementById('sendBtn').disabled = true;

    addMessage(message, 'user');
    input.value = "";
    // Show typing indicator
    document.getElementById('typinIndicator').classList.add('show');
    scrollToBottom();
    
    try {
        // Send to Django backend
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide typing indicator
        document.getElementById('typinIndicator').classList.remove('show');
        
        // Add AI response
        setTimeout(() => {
            addMessage(data.response, 'ai');
            
            // Show crisis banner if needed
            if (data.crisis) {
                document.getElementById('crisisbanner').classList.add('show');
            }
        }, 500);
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('typinIndicator').classList.remove('show');
        addMessage('Sorry, something went wrong. Please try again.', 'ai');
    }
    
    // Re-enable input
    input.disabled = false;
    document.getElementById('sendBtn').disabled = false;
    input.focus();
}

    function addMessage(text, sender) {
            const chatContainer = document.getElementById('chatcontainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const time = new Date().toLocaleTimeString();
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    ${text}
                    <div class="timestamp">${time}</div>
                </div>
            `;
            
            // Insert before typing indicator
            const typingIndicator = document.getElementById('typinIndicator');
            chatContainer.insertBefore(messageDiv, typingIndicator);
            
            scrollToBottom();
        }
        
        function scrollToBottom() {
            const chatContainer = document.getElementById('chatcontainer');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
