"use strict";

document.addEventListener("DOMContentLoaded", function() {
    var chatContainer = document.getElementById('chatContainer');
    var restoreButton = document.getElementById('restoreButton');
    var minimizeButton = document.getElementById('minimizeButton');

    // Minimize and Restore functionality
    minimizeButton.addEventListener('click', function() {
        chatContainer.style.display = 'none';
        restoreButton.style.display = 'block';
    });

    restoreButton.addEventListener('click', function() {
        chatContainer.style.display = 'flex';
        this.style.display = 'none';
    });
    
});
