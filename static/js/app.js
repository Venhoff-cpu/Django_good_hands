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
            e.preventDefault();
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
                let bagWord = "";
                    if (parseInt(bagsInput) === 1){
                        bagWord = "worek";
                    } else if (parseInt(bagsInput) < 5){
                        bagWord = "worki";
                    } else {
                        bagWord = "worków";
                    };
                let stringToPass = bagsInput + " " + bagWord + " rzeczy z kategorii: "
                typeOfDonation.forEach((checkbox, idx, array) => {
                    let description = checkbox.parentElement.lastElementChild.innerHTML.toLowerCase()

                    if (array.length === 1){
                        stringToPass += description + ".";
                    } else if (idx === array.length - 1){
                        stringToPass += description + ".";
                    } else if(idx === 0){
                        stringToPass += description + ", ";
                    } else {
                        stringToPass += description + ", ";
                    };
                });
                typeSummary.innerHTML = stringToPass;

                let charity = form.querySelector("input[name='organization']:checked");
                let charityValue = charity.nextElementSibling.nextElementSibling.querySelector(".title").innerHTML;
                charitySummary.innerHTML = "Dla fundacji " + charityValue + "."
                streetSummary.innerHTML = form.querySelector('#id_street').value;
                citySummary.innerHTML = form.querySelector('#id_city').value;
                zipcodeSummary.innerHTML = form.querySelector('#id_zip_code').value;
                phoneSummary.innerHTML = form.querySelector('#id_phone_number').value;

                pickUpDateSummary.innerHTML = form.querySelector('#id_pick_up_date').value;
                pickUpTimeSummary.innerHTML = form.querySelector('#id_pick_up_time').value;
                let commentary = form.querySelector('#id_pick_up_comment').value
                if (commentary === ""){
                    pickUpCommentSummary.innerHTML = "Brak uwag"
                }else{
                    pickUpCommentSummary.innerHTML = commentary
                };
            }

            summaryBtn.addEventListener("click", (event) => getSummaryInfo())
            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

        }


        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

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
        $.each($("input[name='categories']:checked"), function () {
            console.log($(this).val());
            categories.push($(this).val());
        });
        console.log(categories);
        $.ajax({
            url: "categories/",
            type: "POST",
            data: {
                'categories[]': categories,
            },
            success: function (data) {
                $('#buttons-formInstitutions').before(data)
            },
            error: function () {
                alert('Error')
            },
        })
    });
});
