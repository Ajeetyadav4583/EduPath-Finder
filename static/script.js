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