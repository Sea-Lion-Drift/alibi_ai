<script>

// ==========================================
// ALIBI AI INTERVIEW QUESTIONS
// ==========================================

const questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "Describe a difficult situation you handled.",
    "Where do you see yourself in five years?"
];

let currentQuestion = 0;


// ==========================================
// INTERVIEW TIMER
// ==========================================

let interviewSeconds = 0;

setInterval(function () {

    interviewSeconds++;

    let minutes = Math.floor(interviewSeconds / 60);
    let seconds = interviewSeconds % 60;

    document.getElementById("timer").innerHTML =
        String(minutes).padStart(2, '0') + ":" +
        String(seconds).padStart(2, '0');

}, 1000);


// ==========================================
// ANSWER TIMER
// ==========================================

let answerSeconds = 0;
let answerInterval;

function startAnswerTimer() {

    answerSeconds = 0;

    clearInterval(answerInterval);

    document.getElementById("recordingStatus").style.color = "red";

    answerInterval = setInterval(function () {

        answerSeconds++;

        document.getElementById("recordingStatus").innerHTML =
            "🎙 Listening... " + answerSeconds + " sec";

    }, 1000);

}

function stopAnswerTimer() {

    clearInterval(answerInterval);

    document.getElementById("recordingStatus").style.color = "green";

    document.getElementById("recordingStatus").innerHTML =
        "✔ Answer Submitted";

}


// ==========================================
// AI SPEECH
// ==========================================

function speak(text) {

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);

}


// ==========================================
// START INTERVIEW
// ==========================================

window.onload = function () {

    const introduction = `
Welcome to Alibi AI Interview.

Please ensure your face remains visible throughout the interview.

You will be asked five questions.

Recording will start automatically.

Let's begin.

Question One.

Tell me about yourself.
`;

    speak(introduction);

    startAnswerTimer();

};


// ==========================================
// NEXT QUESTION
// ==========================================

function nextQuestion() {

    stopAnswerTimer();

    currentQuestion++;

    if (currentQuestion < questions.length) {

        document.getElementById("question").innerHTML =
            questions[currentQuestion];

        document.getElementById("questionCount").innerHTML =
            "Question " + (currentQuestion + 1) + " of " + questions.length;

        setTimeout(function () {

            speak("Thank you for your response.");

            setTimeout(function () {

                speak("Question " + (currentQuestion + 1));

                setTimeout(function () {

                    speak(questions[currentQuestion]);

                    startAnswerTimer();

                }, 1200);

            }, 1500);

        }, 700);

    }

    else {

        stopAnswerTimer();

        document.getElementById("recordingStatus").innerHTML =
            "🎉 Interview Completed";

        speak("Congratulations. You have successfully completed the interview. Generating your interview report.");

        setTimeout(function () {

            window.location.href = "/report";

        }, 5000);

    }

}

</script>