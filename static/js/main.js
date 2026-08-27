document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.getElementById("menuButton");
    const navigation = document.getElementById("mainNavigation");

    if (menuButton && navigation) {
        menuButton.addEventListener("click", () => {
            const opened = navigation.classList.toggle("active");

            menuButton.setAttribute(
                "aria-expanded",
                String(opened)
            );

            document.body.classList.toggle(
                "menu-open",
                opened
            );
        });

        navigation.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                navigation.classList.remove("active");
                document.body.classList.remove("menu-open");

                menuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );
            });
        });
    }

    document.querySelectorAll(".message-close").forEach((button) => {
        button.addEventListener("click", () => {
            button.closest(".message")?.remove();
        });
    });

    window.setTimeout(() => {
        document.querySelectorAll(".message").forEach((message) => {
            message.remove();
        });
    }, 7000);

    const mainProductImage =
        document.getElementById("mainProductImage");

    if (mainProductImage) {
        document
            .querySelectorAll(".thumbnail-button")
            .forEach((button) => {
                button.addEventListener("click", () => {
                    if (button.dataset.image) {
                        mainProductImage.src =
                            button.dataset.image;
                    }
                });
            });
    }

    const phoneInput =
        document.querySelector('input[name="phone"]');

    if (phoneInput) {
        phoneInput.addEventListener("input", () => {
            phoneInput.value = phoneInput.value.replace(
                /[^0-9+\-()\s]/g,
                ""
            );
        });
    }

    const slider = document.querySelector("[data-slider]");

    if (slider) {
        const slides = Array.from(
            slider.querySelectorAll("[data-slide]")
        );

        const dots = Array.from(
            slider.querySelectorAll("[data-slider-dot]")
        );

        const previousButton = slider.querySelector(
            "[data-slider-previous]"
        );

        const nextButton = slider.querySelector(
            "[data-slider-next]"
        );

        let currentIndex = 0;
        let timer = null;
        let touchStartX = 0;

        const showSlide = (index) => {
            currentIndex =
                (index + slides.length) % slides.length;

            slides.forEach((slide, slideIndex) => {
                slide.classList.toggle(
                    "is-active",
                    slideIndex === currentIndex
                );

                slide.setAttribute(
                    "aria-hidden",
                    slideIndex === currentIndex
                        ? "false"
                        : "true"
                );
            });

            dots.forEach((dot, dotIndex) => {
                dot.classList.toggle(
                    "is-active",
                    dotIndex === currentIndex
                );

                dot.setAttribute(
                    "aria-selected",
                    dotIndex === currentIndex
                        ? "true"
                        : "false"
                );
            });
        };

        const stopAutomaticChange = () => {
            if (timer) {
                window.clearInterval(timer);
                timer = null;
            }
        };

        const startAutomaticChange = () => {
            stopAutomaticChange();

            timer = window.setInterval(() => {
                showSlide(currentIndex + 1);
            }, 6000);
        };

        previousButton?.addEventListener("click", () => {
            showSlide(currentIndex - 1);
            startAutomaticChange();
        });

        nextButton?.addEventListener("click", () => {
            showSlide(currentIndex + 1);
            startAutomaticChange();
        });

        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => {
                showSlide(index);
                startAutomaticChange();
            });
        });

        slider.addEventListener("mouseenter", stopAutomaticChange);
        slider.addEventListener("mouseleave", startAutomaticChange);
        slider.addEventListener("focusin", stopAutomaticChange);
        slider.addEventListener("focusout", startAutomaticChange);

        slider.addEventListener("touchstart", (event) => {
            touchStartX = event.changedTouches[0].clientX;
        });

        slider.addEventListener("touchend", (event) => {
            const difference =
                event.changedTouches[0].clientX - touchStartX;

            if (Math.abs(difference) < 50) {
                return;
            }

            if (difference > 0) {
                showSlide(currentIndex - 1);
            } else {
                showSlide(currentIndex + 1);
            }

            startAutomaticChange();
        });

        document.addEventListener(
            "visibilitychange",
            () => {
                if (document.hidden) {
                    stopAutomaticChange();
                } else {
                    startAutomaticChange();
                }
            }
        );

        showSlide(0);
        startAutomaticChange();
    }
});