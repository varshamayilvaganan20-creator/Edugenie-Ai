// ============================================================
// EduGenie - Frontend JavaScript
// ============================================================

// Get HTML elements
const taskSelect = document.getElementById("task");
const inputText = document.getElementById("inputText");
const generateBtn = document.getElementById("generateBtn");
const clearBtn = document.getElementById("clearBtn");

const resultBox = document.getElementById("result");
const errorBox = document.getElementById("error");


// ============================================================
// API CALL FUNCTION
// ============================================================

async function callAPI(endpoint, text) {

    const response = await fetch(endpoint, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            text: text
        })
    });


    // Read server response as text first.
    // This prevents "Unexpected token 'I'" JSON errors
    // when the backend returns an Internal Server Error.
    const rawText = await response.text();


    let data;

    try {

        data = JSON.parse(rawText);

    } catch (error) {

        throw new Error(
            "EduGenie server is temporarily unavailable. Please try again in a few seconds."
        );

    }


    // Handle HTTP errors
    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.message ||
            "Something went wrong. Please try again."
        );

    }


    return data;
}


// ============================================================
// DISPLAY RESULT
// ============================================================

function showResult(data) {

    // Hide error
    errorBox.style.display = "none";

    // Show result
    resultBox.style.display = "block";


    // If backend returns plain text
    if (typeof data === "string") {

        resultBox.innerText = data;

        return;
    }


    // Explanation response
    if (data.explanation) {

        resultBox.innerText = data.explanation;

        return;
    }


    // Q&A response
    if (data.answer) {

        resultBox.innerText = data.answer;

        return;
    }


    // Summary response
    if (data.summary) {

        resultBox.innerText = data.summary;

        return;
    }


    // Quiz response
    if (data.questions) {

        resultBox.innerText =
            JSON.stringify(data.questions, null, 2);

        return;
    }


    // Learning path response
    if (data.steps) {

        resultBox.innerText =
            JSON.stringify(data.steps, null, 2);

        return;
    }


    // Fallback
    resultBox.innerText =
        JSON.stringify(data, null, 2);
}


// ============================================================
// DISPLAY ERROR
// ============================================================

function showError(message) {

    // Hide result
    resultBox.style.display = "none";

    // Show error
    errorBox.style.display = "block";

    errorBox.innerText = message;
}


// ============================================================
// GENERATE BUTTON
// ============================================================

generateBtn.addEventListener("click", async () => {

    const text = inputText.value.trim();


    // Check empty input
    if (!text) {

        showError(
            "Please enter a topic or question."
        );

        return;
    }


    // Disable button while processing
    generateBtn.disabled = true;

    generateBtn.innerText = "Generating...";


    // Hide previous error
    errorBox.style.display = "none";


    try {

        let endpoint;


        // Select API endpoint
        switch (taskSelect.value) {

            case "qa":

                endpoint = "/qa";

                break;


            case "explain":

                endpoint = "/explain";

                break;


            case "quiz":

                endpoint = "/quiz";

                break;


            case "summarize":

                endpoint = "/summarize";

                break;


            case "learning":

                endpoint = "/learn/recommendations";

                break;


            default:

                throw new Error(
                    "Please select a valid task."
                );
        }


        // Call backend
        const data = await callAPI(
            endpoint,
            text
        );


        // Display response
        showResult(data);

    }


    catch (error) {

        console.error(
            "EduGenie Error:",
            error
        );


        showError(
            error.message
        );

    }


    finally {

        // Enable button again
        generateBtn.disabled = false;

        generateBtn.innerText = "✨ Generate";
    }

});


// ============================================================
// CLEAR BUTTON
// ============================================================

clearBtn.addEventListener("click", () => {

    // Clear input
    inputText.value = "";


    // Clear result
    resultBox.innerText = "";

    resultBox.style.display = "none";


    // Clear error
    errorBox.innerText = "";

    errorBox.style.display = "none";

});


// ============================================================
// ENTER KEY SUPPORT
// ============================================================

inputText.addEventListener("keydown", (event) => {

    // Ctrl + Enter or Enter from textarea
    if (event.ctrlKey && event.key === "Enter") {

        generateBtn.click();

    }

});


// ============================================================
// INITIAL STATE
// ============================================================

resultBox.style.display = "none";

errorBox.style.display = "none";