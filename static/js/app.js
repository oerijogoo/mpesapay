var message_timer = document.getElementById("message-timer");

setTimeout(function(){
    message_timer.style.display = "none"

},3000)

// Update copyright year
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    } else {
        console.error('Current year element not found');
    }