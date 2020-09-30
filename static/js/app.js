document.addEventListener("DOMContentLoaded", function () {
    console.log('document is ready. I can sleep now');

    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            // e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    const summaryBtn = document.querySelector("#to-summary")
    const typeSummary = document.querySelector('#summary-donation');
    const charitySummary = document.querySelector('#summary-foundation');
    const streetSummary = document.querySelector('#summary-street');
    const citySummary = document.querySelector('#summary-city');
    const zipcodeSummary = document.querySelector('#summary-zip-code');
    const phoneSummary = document.querySelector('#summary-phone');
    const pickUpDateSummary = document.querySelector('#summary-pick-up-date');
    const pickUpTimeSummary = document.querySelector('#summary-pick-up-time');
    const pickUpCommentSummary = document.querySelector('#summary-comment');

    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    if (!this.validateStep(this.currentStep)) {
                        return;
                    }
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            function getSummaryInfo() {
                let typeOfDonation = form.querySelectorAll(`input[name="categories"]:checked`);
                let bagsInput = form.querySelector("#id_quantity").value;
                let bagCount = parseInt(bagsInput);

                let bagWord = "";
                if (bagCount === 1) {
                    bagWord = "worek";
                } else if (bagCount < 5) {
                    bagWord = "worki";
                } else {
                    bagWord = "worków";
                }
                ;
                let stringToPass = bagsInput + " " + bagWord + " rzeczy z kategorii: "
                typeOfDonation.forEach((checkbox, idx, array) => {
                    let description = checkbox.parentElement.lastElementChild.innerHTML.toLowerCase()

                    if (array.length === 1) {
                        stringToPass += description + ".";
                    } else if (idx === array.length - 1) {
                        stringToPass += description + ".";
                    } else if (idx === 0) {
                        stringToPass += description + ", ";
                    } else {
                        stringToPass += description + ", ";
                    }
                    ;
                });
                typeSummary.innerHTML = stringToPass;

                let charity = form.querySelector("input[name='institution']:checked");
                let charityValue = charity.nextElementSibling.nextElementSibling.querySelector(".title").innerHTML;
                charitySummary.innerHTML = "Dla fundacji " + charityValue + "."
                streetSummary.innerHTML = form.querySelector('#id_street').value;
                citySummary.innerHTML = form.querySelector('#id_city').value;
                zipcodeSummary.innerHTML = form.querySelector('#id_zip_code').value;
                phoneSummary.innerHTML = form.querySelector('#id_phone_number').value;

                pickUpDateSummary.innerHTML = form.querySelector('#id_pick_up_date').value;
                pickUpTimeSummary.innerHTML = form.querySelector('#id_pick_up_time').value;
                let commentary = form.querySelector('#id_pick_up_comment').value
                if (commentary === "") {
                    pickUpCommentSummary.innerHTML = "Brak uwag"
                } else {
                    pickUpCommentSummary.innerHTML = commentary
                }
                ;
            }

            // Step 5 - form summary
            summaryBtn.addEventListener("click", (event) => getSummaryInfo())

            // Form submit
            this.$form.querySelector("#form-submit").addEventListener("click", e => this.submit(e));
        }

        /**
         * Form validation
         * Prevents moving up a next slide unless all necessary inputs are provided or corrected
         */
        validateStep(step) {
            let stepForValidation = formValidation.querySelector(`[data-step=${CSS.escape(step)}]`);
            let stepTextInputs = stepForValidation.querySelectorAll("input[type='text']");
            let stepNumberInput = stepForValidation.querySelector("input[type='number']");
            let stepCheckboxInputs = stepForValidation.querySelectorAll(`input[name="categories"]:checked`)
            let stepRadioInput = stepForValidation.querySelector("input[name='institution']:checked")
            console.log(stepRadioInput)
            console.log(stepForValidation)
            if (stepTextInputs.length !== 0) {
                for (let i = 0; i < stepTextInputs.length; i++) {
                    if (stepTextInputs[i].id === "id_pick_up_date") {
                        if (!validateDate(stepTextInputs[i])) {
                            return false;
                        }
                    } else if (stepTextInputs[i].id === "id_zip_code") {
                        if (!validateZipCode(stepTextInputs[i])) {
                            return false;
                        }
                    } else if (stepTextInputs[i].id === "id_pick_up_time") {
                        if (!validatePickUpTime(stepTextInputs[i])) {
                            return false;
                        }
                    } else if (stepTextInputs[i].id === "id_phone_number") {
                        if (!validatePhone(stepTextInputs[i])) {
                            return false;
                        }
                    } else if (stepTextInputs[i].value === "") {
                        stepTextInputs[i].focus();
                        alert("Proszę wypełnić zaznaczone pole")
                        return false;
                        };
                    };
            } else if (stepNumberInput) {
                let num = stepNumberInput.value
                if (num < 1 || num >= 10 || num % 1 !== 0) {
                    stepNumberInput.focus();
                    alert("Ilość worków musi być w przedziale 1 - 10. Nie mogą być podane połówki");
                    return false;
                    }
            } else if (stepCheckboxInputs.length === 0 && step === 1) {
                alert("Należy zaznaczyć przynajmniej jedną z opcji")
                return false;
            } else if (!stepRadioInput && step == 3) {
                alert("Należy wybrac organizację której chcesz przekazać dary")
                return false;
            };
            return true;

            function validateDate(inputText) {
                let dateformat = /^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/]\d{4}$/;
                // Match the date format through regular expression
                if (inputText.value.match(dateformat)) {
                    // Extract the string into month, date and year
                    let pdate = inputText.value.split('/');

                    let dd = parseInt(pdate[0]);
                    let mm = parseInt(pdate[1]);
                    let yy = parseInt(pdate[2]);
                    // Create list of days of a month [assume there is no leap year by default]
                    let ListofDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
                    if (mm == 1 || mm > 2) {
                        if (dd > ListofDays[mm - 1]) {
                            alert('Invalid date format!');
                            return false;
                        }
                    }
                    if (mm == 2) {
                        let lyear = false;
                        if ((!(yy % 4) && yy % 100) || !(yy % 400)) {
                            lyear = true;
                        }
                        if ((lyear == false) && (dd >= 29)) {
                            alert('Invalid date format!');
                            return false;
                        }
                        if ((lyear == true) && (dd > 29)) {
                            alert('Invalid date format!');
                            return false;
                        }
                    }
                    // Verify if provided date is from the past
                    let dateNow = new Date()
                    let match = /(\d+)\/(\d+)\/(\d+)/.exec(inputText.value)
                    let dateProvided = new Date(Date.UTC(match[3], match[2]-1, match[1]));

                    if (dateNow >= dateProvided) {
                        inputText.focus();
                        alert('Data odbioru nie może być z przeszłości!');
                        return false;
                    }
                } else {
                    inputText.focus();
                    alert("Invalid date format!");
                    return false;
                }
                return true;
            };

            function validateZipCode(inputText) {
                let zipCodeFormat = /^\d{2}-\d{3}$/;
                if (inputText.value.match(zipCodeFormat)) {
                    return true;
                } else {
                    inputText.focus();
                    alert("Niepoprawny kod pocztowy! Format 00-000.")
                    return false;
                }
            };

            function validatePhone(inputText) {
                let phoneFormat = /^\+?1?\d{8,12}$/
                if (!inputText.value.match(phoneFormat)) {
                    inputText.focus();
                    alert("Niepoprawny format numeru! Prosze podać numer stacjonarny lub komórkowy.")
                    return false;
                }
                return true;
            };

            function validatePickUpTime(inputText) {
                let timeFormat = /^([0-1]?[0-9]|[2][1-3])[:]([0-5][0-9])/;

                if (inputText.value.match(timeFormat)) {
                    // Extract the string into month, date and year
                    let pdate = inputText.value.split(':');

                    let hh = parseInt(pdate[0], 10);
                    let mm = parseInt(pdate[1], 10);

                    if (20 > hh && 8 > hh) {
                        inputText.focus();
                        alert("Odbiór musi być w godzinach 08:00 - 20:00");
                        return false;
                    };
                    return true;
                } else {
                    inputText.focus();
                    alert("Niepoprawny format godzin. Poprawny format jest w przedzaile 00:00 - 23:59");
                    return false;
                };
            };
        };
        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

        };


        /**
         * Submit form
         *
         *
         */
        submit(e) {
            e.preventDefault();
            $.ajax({
                data: $("#form-id").serialize(),
                type: $("#form-id").attr('method'),
                url: $("#form-id").attr('action'),
                success: function (data) {
                    console.log("success");
                    window.location.href = data.url;
                },
                error: function () {
                    console.log('failure');
                },
            });
            // this.currentStep++;
            // this.updateForm();
        };
    };

    const formValidation = document.querySelector("#form-id")
    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $(form).on('click', '#categories-setup', function () {
        let categories = [];
        let url = $("#formInstitutions").attr("institutions-url");
        $.each($("input[name='categories']:checked"), function () {
            categories.push($(this).val());
        });
        $.ajax({
            url: url,
            type: "POST",
            data: {
                'categories[]': categories,
            },
            success: function (data) {
                if ($('#form-ajax-institutions').length) {
                    console.log('Replaced institutions')
                    $('#form-ajax-institutions').replaceWith(data);
                } else{
                    console.log('Added new institutions')
                    $('#buttons-formInstitutions').before(data)
                };

            },
            error: function () {
                alert('Error')
            },
        });
    });
});
