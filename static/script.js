document.addEventListener("DOMContentLoaded", () => {

    const bookmarks =
    document.querySelectorAll(".bookmark");

    bookmarks.forEach((bookmark, index) => {

        const saved =
        localStorage.getItem(`bookmark-${index}`);

        if(saved === "true"){

            bookmark.classList.remove("fa-regular");

            bookmark.classList.add("fa-solid");

            bookmark.style.color = "#facc15";
        }

        bookmark.addEventListener("click", () => {

            bookmark.classList.toggle("fa-solid");

            bookmark.classList.toggle("fa-regular");

            if(bookmark.classList.contains("fa-solid")){

                bookmark.style.color = "#facc15";

                localStorage.setItem(
                    `bookmark-${index}`,
                    "true"
                );

            }else{

                bookmark.style.color = "";

                localStorage.removeItem(
                    `bookmark-${index}`
                );
            }

        });

    });

});
const forms =
document.querySelectorAll("form");

forms.forEach(form => {

    form.addEventListener("submit", () => {

        const button =
        form.querySelector("button");

        if(button){

            button.innerHTML =
            "Loading...";

            button.disabled = true;
        }

    });

});
let timeLeft = 25 * 60;
let timerInterval = null;

function updateTimerDisplay() {
    const timer = document.getElementById("timer");

    if (!timer) return;

    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;

    timer.textContent =
        `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}

function startTimer() {
    if (timerInterval) return;

    timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);
            timerInterval = null;
            alert("Focus session completed!");
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
}

function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    timeLeft = 25 * 60;
    updateTimerDisplay();
}

updateTimerDisplay();