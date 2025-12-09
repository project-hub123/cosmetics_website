/* ============================================================
   Основной JS для сайта производителя косметики
   ============================================================ */


/* ------------------------------
   Переключение темы (обычная / для слабовидящих)
--------------------------------*/
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggle-style");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            // Переходим на маршрут Flask, который меняет стиль
            window.location.href = "/toggle-style";
        });
    }
});


/* ------------------------------
   КНОПКА "НАВЕРХ"
--------------------------------*/
const scrollTopBtn = document.createElement("div");
scrollTopBtn.id = "scrollTopBtn";
scrollTopBtn.innerHTML = "▲";
scrollTopBtn.style.position = "fixed";
scrollTopBtn.style.bottom = "30px";
scrollTopBtn.style.right = "30px";
scrollTopBtn.style.background = "#ba6e93";
scrollTopBtn.style.color = "#fff";
scrollTopBtn.style.fontSize = "26px";
scrollTopBtn.style.borderRadius = "50%";
scrollTopBtn.style.width = "50px";
scrollTopBtn.style.height = "50px";
scrollTopBtn.style.display = "flex";
scrollTopBtn.style.justifyContent = "center";
scrollTopBtn.style.alignItems = "center";
scrollTopBtn.style.cursor = "pointer";
scrollTopBtn.style.display = "none";
scrollTopBtn.style.zIndex = "999";

document.body.appendChild(scrollTopBtn);

window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        scrollTopBtn.style.display = "flex";
    } else {
        scrollTopBtn.style.display = "none";
    }
});

scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});


/* ------------------------------
   АНИМАЦИЯ ПОЯВЛЕНИЯ КАРТОЧЕК
--------------------------------*/
const cards = document.querySelectorAll(".card");

const appearOptions = {
    threshold: 0.2,
};

const appearOnScroll = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("card-visible");
        appearOnScroll.unobserve(entry.target);
    });
}, appearOptions);

cards.forEach((card) => {
    card.classList.add("card-hidden");
    appearOnScroll.observe(card);
});


/* ------------------------------
   Подсветка активной ссылки меню
--------------------------------*/
const currentUrl = window.location.pathname;
const navLinks = document.querySelectorAll("nav a");

navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentUrl) {
        link.style.fontWeight = "bold";
        link.style.textDecoration = "underline";
    }
});


/* ------------------------------
   Мобильное меню
--------------------------------*/
const burger = document.getElementById("burger");
const mobileMenu = document.getElementById("mobile-menu");

if (burger && mobileMenu) {
    burger.addEventListener("click", () => {
        mobileMenu.classList.toggle("open");
    });
}


/* ------------------------------
   Улучшение UX форм — автофокус на первом input
--------------------------------*/
const firstInput = document.querySelector("form input");
if (firstInput) {
    firstInput.focus();
}
