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

/* ===================== SCROLL REVEAL ===================== */
document.addEventListener("DOMContentLoaded", () => {

    const revealEls = document.querySelectorAll(".reveal");

    if (revealEls.length) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealEls.forEach(el => revealObserver.observe(el));
    }

    /* ===================== PROGRESS / LINE BARS ===================== */
    const lines = document.querySelectorAll(".line");
    const progressBars = document.querySelectorAll(".progress");

    if (lines.length) {
        const lineObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const inner = entry.target.querySelector("span");
                    if (inner) {
                        const targetWidth = inner.style.width || "0%";
                        entry.target.style.setProperty("--target-width", targetWidth);
                        entry.target.classList.add("in-view");
                    }
                    lineObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        lines.forEach(bar => lineObserver.observe(bar));
    }

    if (progressBars.length) {
        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    progressObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        progressBars.forEach(bar => progressObserver.observe(bar));
    }

    /* ===================== NUMBER COUNT-UP ===================== */
    const counters = document.querySelectorAll("[data-count]");

    if (counters.length) {
        const animateCount = (el) => {
            const raw = el.dataset.count;
            const match = raw.match(/^([\d.,]+)(.*)$/);
            if (!match) return;

            const numPart = parseFloat(match[1].replace(/,/g, ""));
            const suffix = match[2] || "";
            const isDecimal = match[1].includes(".");
            const duration = 1400;
            const start = performance.now();

            const step = (now) => {
                const progress = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = numPart * eased;

                el.textContent = isDecimal
                    ? current.toFixed(1) + suffix
                    : Math.floor(current).toLocaleString() + suffix;

                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            };

            requestAnimationFrame(step);
        };

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });

        counters.forEach(el => counterObserver.observe(el));
    }

    /* ===================== SCROLL PROGRESS BAR ===================== */
    const progressBar = document.getElementById("scrollProgressBar");

    if (progressBar) {
        const updateProgress = () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const percent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            progressBar.style.width = percent + "%";
        };

        window.addEventListener("scroll", updateProgress, { passive: true });
        updateProgress();
    }

});
