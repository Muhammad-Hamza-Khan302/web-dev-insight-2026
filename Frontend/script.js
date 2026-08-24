const API_URL = "https://bubbly-celebration-production-1430.up.railway.app/chat";


const questionInput =
    document.getElementById("questionInput");

const sendButton =
    document.getElementById("sendButton");

const chatArea =
    document.getElementById("chatArea");

const hero =
    document.getElementById("hero");

const clearButton =
    document.getElementById("clearButton");



/* -------------------------------- */
/* SEND MESSAGE                     */
/* -------------------------------- */

async function sendMessage() {

    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    // Show welcome screen disappearing
    hero.classList.add("hidden");


    // Add user's message
    addMessage(
        question,
        "user"
    );


    // Clear input
    questionInput.value = "";

    autoResize();


    // Disable send button
    sendButton.disabled = true;


    // Show loading message
    const loadingMessage =
        addLoadingMessage();


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        // Remove loading message
        loadingMessage.remove();


        if (!response.ok) {

            let errorMessage =
                "Something went wrong.";

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage =
                        errorData.detail;
                }

            } catch (error) {
                // Keep default error
            }


            addMessage(
                "Error: " + errorMessage,
                "ai"
            );

            return;
        }


        const data =
            await response.json();


        // Display AI answer
        addMessage(
            data.answer,
            "ai"
        );


    } catch (error) {

        loadingMessage.remove();


        addMessage(
            "Unable to connect to the backend. Please try again.",
            "ai"
        );


        console.error(
            "Backend error:",
            error
        );

    } finally {

        sendButton.disabled = false;

        questionInput.focus();
    }
}



/* -------------------------------- */
/* ADD MESSAGE                      */
/* -------------------------------- */

function addMessage(
    message,
    sender
) {

    const messageContainer =
        document.createElement("div");


    messageContainer.className =
        "message " + sender;


    const content =
        document.createElement("div");


    content.className =
        "message-content";


    content.textContent =
        message;


    messageContainer.appendChild(
        content
    );


    chatArea.appendChild(
        messageContainer
    );


    scrollToBottom();


    return messageContainer;
}



/* -------------------------------- */
/* LOADING MESSAGE                  */
/* -------------------------------- */

function addLoadingMessage() {

    const messageContainer =
        document.createElement("div");


    messageContainer.className =
        "message ai";


    const content =
        document.createElement("div");


    content.className =
        "message-content loading";


    content.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;


    messageContainer.appendChild(
        content
    );


    chatArea.appendChild(
        messageContainer
    );


    scrollToBottom();


    return messageContainer;
}



/* -------------------------------- */
/* SCROLL CHAT                      */
/* -------------------------------- */

function scrollToBottom() {

    chatArea.scrollTop =
        chatArea.scrollHeight;
}



/* -------------------------------- */
/* TEXTAREA AUTO RESIZE             */
/* -------------------------------- */

function autoResize() {

    questionInput.style.height =
        "auto";


    questionInput.style.height =
        Math.min(
            questionInput.scrollHeight,
            150
        ) + "px";
}



/* -------------------------------- */
/* ENTER KEY                        */
/* -------------------------------- */

questionInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);



/* -------------------------------- */
/* INPUT RESIZE                     */
/* -------------------------------- */

questionInput.addEventListener(
    "input",
    autoResize
);



/* -------------------------------- */
/* SEND BUTTON                      */
/* -------------------------------- */

sendButton.addEventListener(
    "click",
    sendMessage
);



/* -------------------------------- */
/* CLEAR CHAT                       */
/* -------------------------------- */

clearButton.addEventListener(
    "click",
    function () {

        chatArea.innerHTML = "";

        hero.classList.remove(
            "hidden"
        );

        questionInput.value = "";

        autoResize();

        questionInput.focus();
    }
);