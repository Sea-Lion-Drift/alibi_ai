// ======================================
// ALIBI AI INTERVIEW ENGINE
// ======================================

// Questions
const questions = [
    "Tell me about yourself.",
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "Describe a difficult situation you handled.",
    "Where do you see yourself in five years?"
];

let currentQuestion = 0;

// ======================================
// Timers
// ======================================

let interviewSeconds = 0;
let answerSeconds = 0;
let answerTimer;

// ======================================
// Speech To Text
// ======================================

let recognition;

let transcript = "";

let allAnswers = [];

if ("webkitSpeechRecognition" in window) {

    recognition = new webkitSpeechRecognition();

} else {

    recognition = new SpeechRecognition();

}

recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = "en-US";

recognition.onresult = function(event){

    transcript = "";

    for(let i=0;i<event.results.length;i++){

        transcript += event.results[i][0].transcript;

    }

    document.getElementById("answer").value = transcript;

};

recognition.onerror = function(){

    console.log("Speech Recognition Error");

};


// ======================================
// Interview Timer
// ======================================

setInterval(function(){

    interviewSeconds++;

    const min = Math.floor(interviewSeconds/60);
    const sec = interviewSeconds%60;

    document.getElementById("timer").innerHTML =
        String(min).padStart(2,"0")
        + ":"
        + String(sec).padStart(2,"0");

},1000);


// ======================================
// AI Voice
// ======================================

function speak(text){

    speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang="en-US";
    speech.rate=1;
    speech.pitch=1;

    speech.onend=function(){

        startListening();

    };

    speechSynthesis.speak(speech);

}


// ======================================
// Speech Recognition
// ======================================

function startListening(){

    transcript="";

    document.getElementById("answer").value="";

    document.getElementById("recordingStatus").innerHTML =
    "🎤 Listening...";

    document.getElementById("recordingStatus").style.color="red";

    recognition.start();

    startAnswerTimer();

}

function stopListening(){

    recognition.stop();

    stopAnswerTimer();

    document.getElementById("recordingStatus").innerHTML =
    "✔ Answer Saved";

    document.getElementById("recordingStatus").style.color="green";

}


// ======================================
// Answer Timer
// ======================================

function startAnswerTimer(){

    answerSeconds=0;

    clearInterval(answerTimer);

    answerTimer=setInterval(function(){

        answerSeconds++;

        document.getElementById("recordingStatus").innerHTML =
        "🎤 Listening... " + answerSeconds + " sec";

    },1000);

}

function stopAnswerTimer(){

    clearInterval(answerTimer);

}


// ======================================
// Start Interview
// ======================================

function startInterview(){

    const intro = `
Welcome to Alibi AI Interview.

Please ensure your face remains visible throughout the interview.

You will be asked five questions.

Recording will start automatically.

Let's begin.

Question One.

${questions[0]}
`;

    document.getElementById("question").innerHTML = questions[0];

    speak(intro);

}


// ======================================
// Next Question
// ======================================

function nextQuestion(){

    stopListening();

    allAnswers.push(transcript);

    console.log(allAnswers);

    currentQuestion++;

    if(currentQuestion<questions.length){

        document.getElementById("question").innerHTML =
        questions[currentQuestion];

        document.getElementById("questionCount").innerHTML =
        "Question " +
        (currentQuestion+1) +
        " of " +
        questions.length;

        setTimeout(function(){

            speak(
                "Thank you for your response. Question " +
                (currentQuestion+1) +
                ". " +
                questions[currentQuestion]
            );

        },1000);

    }

    else{

        speak("Congratulations. The interview has been completed.");

        console.log(allAnswers);

        setTimeout(function(){

            window.location.href="/report";

        },4000);

    }

}


// ======================================
// Page Loaded
// ======================================

window.onload=function(){

    startInterview();

};