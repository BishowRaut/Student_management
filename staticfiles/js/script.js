"use strict";

/**
 * =========================================================
 * STUDENT MANAGEMENT SYSTEM
 * GLOBAL JAVASCRIPT
 *
 * Features:
 * - Delete confirmation
 * - Logout confirmation
 * - Password show / hide
 * - Form validation
 * - Email validation
 * - Age / number validation
 * - Password confirmation
 * - Django message auto-dismiss
 * - Dashboard card interaction
 * - Student search UI
 * - Page loader
 * - Accessibility support
 *
 * IMPORTANT:
 * JavaScript provides UI validation only.
 * Authentication, authorization, permissions and
 * server-side validation are handled by Django.
 * =========================================================
 */


/* =========================================================
   APPLICATION
========================================================= */

const StudentManagement = (() => {

    /* =====================================================
       INITIALIZE APPLICATION
    ===================================================== */

    function init() {

        initializeDeleteConfirmation();

        initializeLogoutConfirmation();

        initializePasswordToggle();

        initializeFormValidation();

        initializeInputValidation();

        initializeAutoDismissMessages();

        initializeDashboardCards();

        initializeSearch();

        initializePageLoader();

    }


    /* =====================================================
       DELETE CONFIRMATION
    ===================================================== */

    function initializeDeleteConfirmation() {

        const deleteForms =
            document.querySelectorAll(".delete-form");


        if (!deleteForms.length) {
            return;
        }


        deleteForms.forEach((form) => {

            form.addEventListener("submit", (event) => {

                const confirmed = window.confirm(
                    "Are you sure you want to delete this student?"
                );


                if (!confirmed) {

                    event.preventDefault();

                }

            });

        });

    }


    /* =====================================================
       LOGOUT CONFIRMATION
    ===================================================== */

    function initializeLogoutConfirmation() {

        const logoutForms =
            document.querySelectorAll(".logout-form");


        if (!logoutForms.length) {
            return;
        }


        logoutForms.forEach((form) => {

            form.addEventListener("submit", (event) => {

                const confirmed = window.confirm(
                    "Are you sure you want to logout?"
                );


                if (!confirmed) {

                    event.preventDefault();

                }

            });

        });

    }


    /* =====================================================
       PASSWORD SHOW / HIDE
    ===================================================== */

    function initializePasswordToggle() {

        const passwordInputs =
            document.querySelectorAll(
                'input[type="password"]'
            );


        if (!passwordInputs.length) {
            return;
        }


        passwordInputs.forEach((input) => {

            const wrapper =
                input.parentElement;


            if (!wrapper) {
                return;
            }


            /*
             * Don't create another button if
             * one already exists.
             */

            if (
                wrapper.querySelector(
                    ".password-toggle"
                )
            ) {

                return;

            }


            wrapper.classList.add(
                "password-wrapper"
            );


            const button =
                document.createElement("button");


            button.type = "button";

            button.className =
                "password-toggle";

            button.textContent = "Show";


            button.setAttribute(
                "aria-label",
                "Show password"
            );


            button.setAttribute(
                "aria-pressed",
                "false"
            );


            wrapper.appendChild(button);


            button.addEventListener(
                "click",
                () => {

                    const isPassword =
                        input.type === "password";


                    input.type =
                        isPassword
                            ? "text"
                            : "password";


                    button.textContent =
                        isPassword
                            ? "Hide"
                            : "Show";


                    button.setAttribute(
                        "aria-label",
                        isPassword
                            ? "Hide password"
                            : "Show password"
                    );


                    button.setAttribute(
                        "aria-pressed",
                        String(isPassword)
                    );


                    /*
                     * Keep cursor inside
                     * the password field.
                     */

                    input.focus();

                }
            );

        });

    }


    /* =====================================================
       FORM VALIDATION INITIALIZATION
    ===================================================== */

    function initializeFormValidation() {

        const forms =
            document.querySelectorAll("form");


        if (!forms.length) {
            return;
        }


        forms.forEach((form) => {

            /*
             * Logout does not need validation.
             */

            if (
                form.classList.contains(
                    "logout-form"
                )
            ) {

                return;

            }


            /*
             * Delete forms are handled
             * separately.
             */

            if (
                form.classList.contains(
                    "delete-form"
                )
            ) {

                return;

            }


            form.addEventListener(
                "submit",
                (event) => {

                    const valid =
                        validateForm(form);


                    if (!valid) {

                        event.preventDefault();

                    }

                }
            );

        });

    }


    /* =====================================================
       FORM VALIDATION ENGINE
    ===================================================== */

    function validateForm(form) {

        let valid = true;

        let firstError = null;


        /* -------------------------------------------------
           REQUIRED FIELDS
        ------------------------------------------------- */

        const requiredFields =
            form.querySelectorAll(
                "[required]"
            );


        requiredFields.forEach((field) => {

            if (
                field.disabled ||
                field.type === "hidden"
            ) {

                return;

            }


            const value =
                getFieldValue(field);


            if (!value) {

                setFieldError(field);

                valid = false;


                if (!firstError) {

                    firstError = field;

                }

            } else {

                clearFieldError(field);

            }

        });


        /* -------------------------------------------------
           EMAIL VALIDATION
        ------------------------------------------------- */

        const emailInputs =
            form.querySelectorAll(
                'input[type="email"]'
            );


        emailInputs.forEach((input) => {

            const email =
                getFieldValue(input);


            /*
             * Empty required fields are already
             * handled by required validation.
             */

            if (!email) {

                return;

            }


            if (!isValidEmail(email)) {

                setFieldError(input);

                valid = false;


                if (!firstError) {

                    firstError = input;

                }

            }

        });


        /* -------------------------------------------------
           NUMBER VALIDATION
        ------------------------------------------------- */

        const numberInputs =
            form.querySelectorAll(
                'input[type="number"]'
            );


        numberInputs.forEach((input) => {

            const value =
                getFieldValue(input);


            if (!value) {

                return;

            }


            const number =
                Number(value);


            if (
                Number.isNaN(number) ||
                !isValidNumberField(
                    input,
                    number
                )
            ) {

                setFieldError(input);

                valid = false;


                if (!firstError) {

                    firstError = input;

                }

            }

        });


        /* -------------------------------------------------
           PASSWORD CONFIRMATION
        ------------------------------------------------- */

        const password =
            form.querySelector(
                'input[name="password1"], ' +
                'input[name="password"]'
            );


        const passwordConfirm =
            form.querySelector(
                'input[name="password2"], ' +
                'input[name="password_confirm"]'
            );


        if (
            password &&
            passwordConfirm &&
            password.value !==
                passwordConfirm.value
        ) {

            setFieldError(
                passwordConfirm
            );


            valid = false;


            if (!firstError) {

                firstError =
                    passwordConfirm;

            }

        }


        /* -------------------------------------------------
           FOCUS FIRST ERROR
        ------------------------------------------------- */

        if (firstError) {

            focusField(firstError);

        }


        return valid;

    }


    /* =====================================================
       GET FIELD VALUE
    ===================================================== */

    function getFieldValue(field) {

        if (
            field.type === "checkbox" ||
            field.type === "radio"
        ) {

            return field.checked
                ? field.value
                : "";

        }


        return field.value.trim();

    }


    /* =====================================================
       EMAIL VALIDATION
    ===================================================== */

    function isValidEmail(email) {

        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


        return emailPattern.test(email);

    }


    /* =====================================================
       NUMBER VALIDATION
    ===================================================== */

    function isValidNumberField(
        input,
        value
    ) {

        /*
         * Student age.
         */

        if (
            input.name === "age" ||
            input.id === "age"
        ) {

            return (
                value >= 1 &&
                value <= 120
            );

        }


        /*
         * Respect HTML min attribute.
         */

        if (
            input.min !== "" &&
            value < Number(input.min)
        ) {

            return false;

        }


        /*
         * Respect HTML max attribute.
         */

        if (
            input.max !== "" &&
            value > Number(input.max)
        ) {

            return false;

        }


        return true;

    }


    /* =====================================================
       SET FIELD ERROR
    ===================================================== */

    function setFieldError(field) {

        field.classList.add(
            "input-error"
        );


        field.setAttribute(
            "aria-invalid",
            "true"
        );

    }


    /* =====================================================
       CLEAR FIELD ERROR
    ===================================================== */

    function clearFieldError(field) {

        field.classList.remove(
            "input-error"
        );


        field.removeAttribute(
            "aria-invalid"
        );

    }


    /* =====================================================
       FOCUS FIELD
    ===================================================== */

    function focusField(field) {

        field.focus();


        /*
         * Smooth scrolling is useful for
         * long forms.
         */

        field.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }


    /* =====================================================
       LIVE INPUT VALIDATION
    ===================================================== */

    function initializeInputValidation() {

        document.addEventListener(
            "input",
            (event) => {

                const field =
                    event.target;


                if (
                    !field.matches(
                        "input, textarea, select"
                    )
                ) {

                    return;

                }


                /*
                 * Remove required-field error
                 * once the user enters a value.
                 */

                if (
                    field.classList.contains(
                        "input-error"
                    )
                ) {

                    if (
                        getFieldValue(field)
                    ) {

                        /*
                         * Don't clear an invalid
                         * email or number just because
                         * it contains text.
                         */

                        if (
                            field.type === "email"
                        ) {

                            if (
                                isValidEmail(
                                    getFieldValue(
                                        field
                                    )
                                )
                            ) {

                                clearFieldError(
                                    field
                                );

                            }

                        } else if (
                            field.type === "number"
                        ) {

                            validateNumberField(
                                field
                            );

                        } else {

                            clearFieldError(
                                field
                            );

                        }

                    }

                }


                /*
                 * Live number validation.
                 */

                if (
                    field.matches(
                        'input[type="number"]'
                    )
                ) {

                    validateNumberField(
                        field
                    );

                }

            }
        );

    }


    /* =====================================================
       LIVE NUMBER VALIDATION
    ===================================================== */

    function validateNumberField(field) {

        const value =
            getFieldValue(field);


        if (!value) {

            clearFieldError(field);

            return;

        }


        const number =
            Number(value);


        if (
            Number.isNaN(number) ||
            !isValidNumberField(
                field,
                number
            )
        ) {

            setFieldError(field);

        } else {

            clearFieldError(field);

        }

    }


    /* =====================================================
       AUTO DISMISS DJANGO MESSAGES
    ===================================================== */

    function initializeAutoDismissMessages() {

        const messages =
            document.querySelectorAll(
                ".message, " +
                ".alert, " +
                ".messages li"
            );


        if (!messages.length) {

            return;

        }


        messages.forEach((message) => {

            /*
             * Error messages stay visible
             * longer than success messages.
             */

            const isError =
                message.classList.contains(
                    "error"
                ) ||
                message.classList.contains(
                    "danger"
                );


            const delay =
                isError
                    ? 8000
                    : 5000;


            setTimeout(() => {

                message.classList.add(
                    "message-hide"
                );


                /*
                 * Wait for CSS transition.
                 */

                setTimeout(() => {

                    if (
                        message.parentNode
                    ) {

                        message.remove();

                    }

                }, 400);

            }, delay);

        });

    }


    /* =====================================================
       DASHBOARD CARDS
    ===================================================== */

    function initializeDashboardCards() {

        const cards =
            document.querySelectorAll(
                ".dashboard-card-link"
            );


        if (!cards.length) {

            return;

        }


        cards.forEach((card) => {

            card.addEventListener(
                "click",
                () => {

                    card.classList.add(
                        "card-clicked"
                    );

                }
            );

        });

    }


    /* =====================================================
       SEARCH
    ===================================================== */

    function initializeSearch() {

        const searchInput =
            document.querySelector(
                "#student-search"
            );


        if (!searchInput) {

            return;

        }


        updateSearchState(
            searchInput
        );


        searchInput.addEventListener(
            "input",
            () => {

                updateSearchState(
                    searchInput
                );

            }
        );


        /*
         * Escape clears the search.
         */

        searchInput.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Escape"
                ) {

                    searchInput.value = "";


                    updateSearchState(
                        searchInput
                    );

                }

            }
        );

    }


    /* =====================================================
       SEARCH STATE
    ===================================================== */

    function updateSearchState(
        searchInput
    ) {

        const hasValue =
            getFieldValue(
                searchInput
            ).length > 0;


        searchInput.classList.toggle(
            "search-active",
            hasValue
        );

    }


    /* =====================================================
       PAGE LOADER
    ===================================================== */

    function initializePageLoader() {

        const loader =
            document.getElementById(
                "page-loader"
            );


        if (!loader) {

            return;

        }


        let hidden = false;


        const hideLoader = () => {

            if (hidden) {

                return;

            }


            hidden = true;


            loader.classList.add(
                "loader-hidden"
            );

        };


        /*
         * If the page is already loaded.
         */

        if (
            document.readyState ===
            "complete"
        ) {

            setTimeout(
                hideLoader,
                500
            );

        } else {

            window.addEventListener(
                "load",
                () => {

                    setTimeout(
                        hideLoader,
                        500
                    );

                },
                {
                    once: true
                }
            );

        }


        /*
         * Safety fallback.
         */

        setTimeout(
            hideLoader,
            3000
        );

    }


    /* =====================================================
       PUBLIC API
    ===================================================== */

    return {

        init

    };

})();


/* =========================================================
   START APPLICATION
========================================================= */

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        StudentManagement.init,
        {
            once: true
        }
    );

} else {

    StudentManagement.init();

}