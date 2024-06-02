document.addEventListener("DOMContentLoaded", function() {
    var input = document.querySelector('input[type="text"]');
    var runButton = document.getElementById('runButton');

    input.addEventListener('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            runButton.click();
        }
    });

    runButton.onclick = function() {
        var messageText = input.value.trim();
        if (messageText !== "") {
            var messagesDiv = document.querySelector('.messages');
            var newMessage = document.createElement('div');
            newMessage.className = 'message mine';
            newMessage.textContent = messageText;
            messagesDiv.appendChild(newMessage);
            console.log("Hello, world!");

            var storedJson = sessionStorage.getItem('response');
            var bodyContent = storedJson ? messageText + "##" + storedJson : messageText;
            console.log("Submitting:", bodyContent);

            fetch('/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'text=' + encodeURIComponent(bodyContent)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    var newReply = document.createElement('div');
                    newReply.className = 'message theirs';
                    newReply.textContent = data.text;
                    messagesDiv.appendChild(newReply);

                    if (data.data.time === -1) {
                        sessionStorage.clear();  
                    } else {
                        sessionStorage.setItem('response', JSON.stringify(data.data));  
                    }

                    setTimeout(() => {  
                        if (data.data.time === 2 || data.data.time === 3 || data.data.time === 4) {
                            displayModal(data.data);
                        }
                    }, 100);  

                } else {
                    console.error("Server error:", data.error);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
            });

            input.value = '';
        }
    };
    
    window.addEventListener('unload', function() {
        sessionStorage.clear();
    });

    function displayModal(data) {
        var modalText = `You have a total of ${data.total_people || 0} people, with ${data.adults || 0} adults and ${data.children || 0} children. Your budget is ${data.money || 'unknown'}, departing from ${data.origin}, to ${data.destination}, on approximately ${data.date}.`;
        if (confirm(modalText + " Do you confirm this information is correct?")) {
            submitCachedData();
        } else {
            sessionStorage.clear(); 
            alert("Please re-enter your information.");
        }
    }

    function submitCachedData() {
        var cachedData = sessionStorage.getItem('response');
        if (cachedData) {
            fetch('/submit-cached-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: cachedData
            })
            .then(response => response.json())
            .then(result => {
                alert("Data submitted successfully: " + result.message);
                var answer = result.analysis ? JSON.parse(result.analysis).answer : null;
                if (answer) {
                    try {
                        
                        var answerData = JSON.parse(answer);
               
                        ['ticket_info', 'attraction_info', 'hotel_info', 'cuisine_info'].forEach(key => {
                            if (answerData[key]) {
                                var newMessage = document.createElement('div');
                                newMessage.classList.add('message', 'theirs');
                                
                                var link = document.createElement('a');
                                link.href = answerData[key];
                                link.textContent = key.replace('_', ' ') + ' details';
                                link.target = "_blank"; 
                                newMessage.appendChild(link);
                                appendMessageToChatContainer(newMessage);
                            }
                        });
                    } catch (e) {
                       
                        createMessageElement(answer);
                    }
                }
            })
            .catch(error => {
                console.error("Error submitting cached data:", error);
            });
        }
    }
    
    function appendMessageToChatContainer(messageElement) {
        var chatContainer = document.querySelector('.chat-container');
        var lastMessage = chatContainer.querySelector('.message.mine:last-child, .message.theirs:last-child');
        if (lastMessage) {
            lastMessage.parentNode.insertBefore(messageElement, lastMessage.nextSibling);
        } else {
            chatContainer.appendChild(messageElement);
        }
    }
    
    function createMessageElement(text) {
        var newMessage = document.createElement('div');
        newMessage.classList.add('message', 'theirs');
        newMessage.textContent = text;
        appendMessageToChatContainer(newMessage);
    }
}
);