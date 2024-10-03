// Fetch the necessary DOM elements
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const resultElement = document.getElementById('result');
const questionElement = document.getElementById('question');
const form = document.getElementById('answerForm');
let playerX = 50;
let playerY = 200;
let playerSpeed = 20;
const targetX = 350; // Target position at the end of the canvas
const targetWidth = 50;
let levelFinished = false;
let lives = 3;

// Function to draw the player (a simple rectangle for now)
function drawPlayer() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas before each draw
    ctx.fillStyle = 'blue';
    ctx.fillRect(playerX, playerY, 50, 50); // Draw player as a blue square
    drawTarget(); // Draw the target
}

// Function to draw the target (a red square for now)
function drawTarget() {
    ctx.fillStyle = 'red';
    ctx.fillRect(targetX, playerY, targetWidth, 50); // Target at the end of the canvas
}

// Function to move the player
function movePlayer() {
    // Only move if the level is not finished
    if (!levelFinished) {
        playerX += playerSpeed; // Move player to the right
        drawPlayer(); // Redraw the player in the new position
        checkIfLevelFinished(); // Check if the player has reached the target
    }
}

// Function to check if the player has reached the target
function checkIfLevelFinished() {
    if (playerX + 50 >= targetX) {
        levelFinished = true; // Mark the level as finished
        resultElement.innerText = "Level Finished! Redirecting...";

        // Redirect to the Game Select page after 2 seconds
        setTimeout(() => {
            window.location.href = "/gameselect/"; // Adjust this path based on your URL structure
        }, 2000); // 2 seconds delay before redirecting
    }
}

// Initialize the canvas with the player and target
drawPlayer();

// Function to fetch a new question from the server
async function fetchQuestion() {
    try {
        console.log("Fetching question...");
        const response = await fetch("/generate_question/");
        const data = await response.json();
        console.log("Response received:", response);
        console.log("Data received:", data);
        questionElement.innerText = `Solve: ${data.question}`;
        document.getElementById("correct_answer").value = data.answer;
    } catch (error) {
        console.error("Error fetching question:", error);
    }
}

// Call the fetchQuestion function when the page loads
window.onload = fetchQuestion;

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
    }

    // Optional: Add logic here for when all lives are lost (Game Over)
    if (lives === 0) {
        alert("Game Over!");
        // Redirect to the Game Select page after 2 seconds
        setTimeout(() => {
            window.location.href = "/gameselect/"; // Adjust this path based on your URL structure
        }, 2000); // 2 seconds delay before redirecting
    }
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
                movePlayer();  // Trigger the player movement when the answer is correct
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
    fetchQuestion();
};
