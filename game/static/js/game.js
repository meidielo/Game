// Fetch the necessary DOM elements
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const resultElement = document.getElementById('result');
const questionElement = document.getElementById('question');
const form = document.getElementById('answerForm');

// Dino sprite settings
const SPRITE_WIDTH = 24;  // Width of each frame in the sprite sheet
const SPRITE_HEIGHT = 24; // Height of each frame in the sprite sheet
const FRAMES = 11;
const IDLE_FRAMES = 3;    // Number of frames for idle animation (first 3)
const LOSS_ANIMATION_FRAMES = [15, 16, 17];
// Calculate the scaling factor based on the canvas width (relative scaling)
let scalingFactor = canvas.width / 800; // Use 800 as your default canvas width for scaling

// Scale the player size dynamically based on the canvas size
let playerWidth = 100 * scalingFactor;  // Adjust size as 10% of the canvas width
let playerHeight = 100 * scalingFactor; // Adjust size as 10% of the canvas height

// Adjust the player's X and Y position based on the canvas size
let playerX = canvas.width * 0.1;  // Set X position relative to the canvas width (10% from the left)
let playerY = canvas.height - playerHeight + 10;  // Set Y position relative to the canvas height (70% from the top, adjust for height)

let playerSpeed = 2;  // Reduce speed for smoother movement
let levelFinished = false;
let lives = 3;
let currentFrame = 0;  // Track the current frame for the dino animation
let lastFrameTime = 0; // To handle the frame update timing
const FRAME_DURATION = 100; // Time in milliseconds for each frame
let moving = false;  // Check if the player is moving
let isLosingLife = false;  // Flag to check if life loss animation is happening
let lossFrameIndex = 0; // Track which frame of life loss animation to show

// const PORTAL_WIDTH = 32;   // Adjust width as per your portal sprite frame size
// const PORTAL_HEIGHT = 32;  // Adjust height as per your portal sprite frame size
// const TOTAL_PORTAL_FRAMES = 7; // Number of frames in your portal sprite sheets
// let portalFrame = 0;
// const PORTAL_FRAME_DURATION = 100;  // Adjust for desired animation speed
// let lastPortalFrameTime = 0;

// const targetX = 800; // Target position at the end of the canvas
// let targetPositionX = playerX;  // The position the player is moving toward

let movesMade = 0; // Track how many moves the player has made
let movesBeforeGoal = 3; // Number of moves before the player reaches the goal
let distancePerMove = (canvas.width - playerWidth - 10) / movesBeforeGoal;  // Distance the player moves per question

let backgroundX = 0;  // Starting position of the background
const backgroundSpeed = 2;  // Speed at which the background moves
let backgroundRepeatCount = 0;
let backgroundReachedEnd = false;  // Track if the background has reached the end
const MAX_BACKGROUND_REPEATS = 1;

let stageComplete = false;  // Flag to track if the stage is complete

// Load the background image
const background = new Image();
background.src = '/static/assets/Background.png';

// const portalSpriteSheet = new Image();
// portalSpriteSheet.src = '/static/assets/portal5_spritesheet.png';

const dinoSpriteSheet = new Image();
dinoSpriteSheet.src = '/static/assets/DinoSprites - doux.png';

// Function to draw the background
function drawBackground() {
    if (moving && !backgroundReachedEnd) {
        // Scroll the background by updating its position only if it hasn't reached the end
        backgroundX -= backgroundSpeed;

        // If the background reaches the end, stop moving it
        if (backgroundX <= -canvas.width) {
            backgroundX = 0;
            backgroundRepeatCount++;
        }

        if (backgroundRepeatCount >= MAX_BACKGROUND_REPEATS) {
            backgroundReachedEnd = true;
        }
    }

    // Draw the background twice to create a looping effect
    ctx.drawImage(background, backgroundX, 0, canvas.width, canvas.height);
    ctx.drawImage(background, backgroundX + canvas.width, 0, canvas.width, canvas.height);
}

// Function to draw the entire game screen
function drawScene() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas once here
    drawBackground();  // Draw the background
    drawPlayer();  // Draw the player (including any animations)
    // drawPortals();  // Draw the door (target)
}

// Function to draw the player (using the dino sprite)
function drawPlayer() {

    // Draw dino sprite (based on whether life loss animation is happening)
    if (isLosingLife) {
        ctx.drawImage(
            dinoSpriteSheet,
            LOSS_ANIMATION_FRAMES[lossFrameIndex] * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT,  // Source rectangle
            playerX, playerY, playerWidth, playerHeight
        );
    } else {
        ctx.drawImage(
            dinoSpriteSheet,
            currentFrame * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT,  // Source rectangle
            playerX, playerY, playerWidth, playerHeight
        );
    }
}

// function drawPortals() {
//     const now = Date.now();
//     if (now - lastPortalFrameTime > PORTAL_FRAME_DURATION) {
//         portalFrame = (portalFrame + 1) % TOTAL_PORTAL_FRAMES;
//         lastPortalFrameTime = now;
//     }

//     // Drawing one portal as big as the player, placed on the ground
//     ctx.drawImage(
//         portalSpriteSheet, // Use the first portal sprite sheet or the desired one
//         portalFrame * PORTAL_WIDTH, 0, PORTAL_WIDTH, PORTAL_HEIGHT,  // Source from sprite sheet
//         targetX, playerY + 20, 64, 64  // Adjust size and Y position to match player on the ground
//     );
// }

// Function to move the player when an answer is correct
function movePlayer() {
    const questionElement = document.getElementById("question");
    if (!levelFinished && movesMade < movesBeforeGoal) {
        questionElement.innerText = 'Loading...';
        movesMade++;  // Increment the number of moves made
        moving = true;  // Start smooth movement and walking animation

        setTimeout(() => {
            moving = false;  // Stop moving after a short delay
            if (movesMade < movesBeforeGoal) {
                fetchQuestion(mode);  // Fetch a new question only after finishing the move
            }
        }, 2000);  // Duration for moving and animation (e.g., 2 seconds)
    }
}

// Function to update the animation frame
function updateFrame() {
    const now = Date.now();
    if (now - lastFrameTime > FRAME_DURATION) {
        if (isLosingLife) {
            // Update frame for life loss animation
            lossFrameIndex = (lossFrameIndex + 1) % LOSS_ANIMATION_FRAMES.length;

            // End the life loss animation after playing through the frames
            if (lossFrameIndex === 0) {
                isLosingLife = false; // Stop life loss animation
            }
        } else if (moving) {
            currentFrame = (currentFrame + 1) % FRAMES;
        } else {
            // Loop through the idle frames (first 3 frames) when the player is not moving
            currentFrame = (currentFrame + 1) % IDLE_FRAMES;
        }
        lastFrameTime = now;
    }
}

// Function to animate the game
function animate() {
    if (!levelFinished) {
        // If the player is moving
        if (moving) {
            if (backgroundReachedEnd) {
                // Move the player if the background has stopped moving
                if (playerX < canvas.width - playerWidth - 10) {  // Move player to the end of the canvas
                    playerX += playerSpeed;  // Move the player slightly in each frame
                    if (playerX >= canvas.width - playerWidth - 10) {
                        playerX = canvas.width - playerWidth - 10;  // Snap to end position
                        moving = false;  // Stop moving
                        stageComplete = true;  // Mark the stage as complete
                    }
                }
            }
        }

        updateFrame();  // Update the frame for the sprite animation (idle or moving)
    }

    drawScene();  // Draw everything (background, player, portals, etc.)
    checkIfLevelFinished();  // Check if the player has reached the target

    // Keep the animation loop running
    requestAnimationFrame(animate);

    // Check if the stage is complete
    if (stageComplete) {
        finishStage();  // Call the function to handle stage completion
    }
}


// Function to dynamically display stars based on the number of lives
function showStars(lives) {
    const starsContainer = document.getElementById("starsContainer");
    starsContainer.innerHTML = ""; // Clear any existing stars

    // Use the number of lives to determine how many stars to show
    for (let i = 0; i < lives; i++) {
        const starImg = document.createElement("img");
        starImg.src = "/static/assets/star.png";
        starImg.alt = "Star";
        starsContainer.appendChild(starImg);
    }

    // Send the points to the server
    fetch('/update-points/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Use Django's CSRF token for security
        },
        body: JSON.stringify({ 'points': lives })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Points updated:', data.points);
            } else {
                console.error('Failed to update points');
            }
        });
}

let popupShown = false;

function showLevelCompletePopup(mode) {
    // Check if popup was already shown to avoid multiple calls
    if (!popupShown) {
        popupShown = true;  // Set the flag to true so popup is shown only once

        // Display the popup
        const popup = document.getElementById("levelCompletePopup");
        popup.style.display = "block";

        // Show stars based on lives
        showStars(lives);

        // Check if the mode is "hard" and hide the "Next" button if it is
        if (mode === 'hard') {
            document.getElementById("nextButton").style.display = 'none'; // Hide the Next button
        } else {
            document.getElementById("nextButton").style.display = 'inline-block'; // Show the Next button for other modes
        }

        // Add event listeners to the buttons
        document.getElementById("replayButton").onclick = function () {
            // Replay the current mode
            window.location.href = "/" + mode + "/";
        };

        document.getElementById("nextButton").onclick = function () {
            // Redirect to the next mode based on the current mode
            if (mode === "easy") {
                window.location.href = "/medium/";
            } else if (mode === "medium") {
                window.location.href = "/hard/";
            }
        };

        document.getElementById("gameSelectButton").onclick = function () {
            // Go back to game select
            window.location.href = "/homepage/";
        };
    }
}

// Function to handle stage completion
function finishStage() {
    levelFinished = true;  // Mark the level as finished
    showLevelCompletePopup(mode);  // Show the popup for next action (e.g., next level or replay)
}

// Function to check if the player has reached the end of the level
function checkIfLevelFinished() {
    // This function is redundant if we move the player based on canvas size
    if (playerX + playerWidth >= canvas.width - 10) {
        stageComplete = true;  // Mark stage as complete if player reaches the end
    }
}

// Function to fetch a new question from the server
async function fetchQuestion(mode) {
    try {
        console.log("Fetching question for mode:", mode);
        const response = await fetch(`/generate_question/${mode}/`);
        const data = await response.json();
        console.log("Response received:", response);
        console.log("Data received:", data);
        questionElement.innerText = `Solve: ${data.question}`; 
        document.getElementById("correct_answer").value = data.answer;
    } catch (error) {
        console.error("Error fetching question:", error);
    }
}

// Function to update lives when an incorrect answer is given
function loseLife() {
    if (lives > 0) {
        if (lives === 3) {
            document.getElementById('life3').style.display = 'none';
        } else if (lives === 2) {
            document.getElementById('life2').style.display = 'none';
        } else if (lives === 1) {
            document.getElementById('life1').style.display = 'none';
        }
        lives--;

        // Trigger the life loss animation
        isLosingLife = true;
        lossFrameIndex = 0; // Start from the first loss frame
    }

    // Optional: Add logic here for when all lives are lost (Game Over)
    if (lives === 0) {
        alert("Game Over!");
        // Redirect to the Game Select page after 2 seconds
        setTimeout(() => {
            window.location.href = "/homepage/"; // Adjust this path based on your URL structure
        }, 2000); // 2 seconds delay before redirecting
    }
}

// Helper function to get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Handle the form submission and validate the answer
form.onsubmit = async function (event) {
    event.preventDefault(); // Prevent the form from refreshing the page
    console.log("Submitting form...");

    const formData = new FormData(form);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch("/validate_answer/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrftoken
            }
        });

        console.log("Form response:", response);

        // Check if the response is OK and JSON parseable
        if (response.ok) {
            const result = await response.json();
            console.log("Result received:", result);

            if (result.result === "correct") {
                resultElement.innerText = "Correct! The character will move.";
                movePlayer();  // Trigger the player movement and background scrolling when the answer is correct
            } else {
                document.getElementById("result").innerText = "Incorrect! You lost a life.";
                loseLife();  // Decrease life when answer is wrong
            }
        } else {
            const errorText = await response.text();
            console.error("Error response from server:", errorText);
            resultElement.innerText = "Error submitting form.";
        }
    } catch (error) {
        console.error("Error submitting form:", error);
    }

    // Clear the answer input field regardless of the response
    document.getElementById("user_answer").value = "";

    // Fetch a new question after submitting the answer
    // fetchQuestion(mode);
};

function resizeCanvas() {
    // Resize canvas to fit the screen while keeping a margin
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Set canvas dimensions
    canvas.width = screenWidth * 0.6;
    canvas.height = screenHeight * 0.6;

    // Update scaling factors
    scalingFactor = canvas.width / 800; // Assuming 800 as the default canvas width
    playerWidth = 75 * scalingFactor;
    playerHeight = 75 * scalingFactor;
    playerX = canvas.width * 0.1;
    playerY = canvas.height - playerHeight - 20;
    distancePerMove = (canvas.width - playerWidth + 10) / movesBeforeGoal;

    // Adjust text size for UI
    document.getElementById("question").style.fontSize = `${scalingFactor * 15}px`;
    document.getElementById("result").style.fontSize = `${scalingFactor * 15}px`;

    // Redraw the entire scene after resizing
    drawScene();
}

// Add event listener to resize the canvas whenever the window is resized
window.addEventListener('resize', resizeCanvas);

// Initialize game
function init() {
    resizeCanvas();
    dinoSpriteSheet.onload = function () {
        drawPlayer();  // Draw the initial state
    };

    console.log("Mode:", mode);
    fetchQuestion(mode);  // Fetch the first question
    animate();  // Start the animation loop
}

window.onload = init();