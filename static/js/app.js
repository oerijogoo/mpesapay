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


.intro-section {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1030;
    background-color: #f8f9fa; /* Matches the bg-light class */
    padding: 10px 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
body {
    padding-top: 60px; /* Adjust this based on the height of .intro-section */
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
