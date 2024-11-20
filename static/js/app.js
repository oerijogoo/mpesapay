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




/* Thin Introduction Section */
.intro-section {
    padding: 0.5rem 0; /* Thin height similar to navbar */
    font-size: 0.9rem; /* Small text size */
    border-bottom: 1px solid #ddd; /* Subtle border for separation */
}

/* Prevent Overlap with Navbar */
.navbar + .intro-section {
    margin-top: 56px; /* Matches typical navbar height */
}

/* Card Images */
.card-img-top {
    height: auto;
    max-height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease-in-out;
}

.card-img-top:hover {
    transform: scale(1.05);
}

/* Responsive Scaling */
@media (max-width: 768px) {
    .card-img-top {
        max-height: 150px;
    }
}

@media (max-width: 576px) {
    .card-img-top {
        max-height: 100px;
    }
}
