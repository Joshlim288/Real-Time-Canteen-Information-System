// TODO Ajax error handling
const appUrl = "http://127.0.0.1:5000/";
const dateFormat = "YYYY-MM-DD HH:mm:ss";
const indexUrl = [appUrl, appUrl + "restaurants", appUrl + "restaurants/"];

// Reset Datetime picker if in any default url.
var currentUrl = window.location.href;
if($.inArray(currentUrl, indexUrl) > -1 || !isNaN(window.location.pathname.split('/').slice(2,3).join('/'))) {
    localStorage.setItem("queryDatetime", "");
}

var queryDatetime = "";

function currentTimeClock() {
    var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds()),
        timeDisplay = document.getElementById("tt");

    function checkTime(i) {
        if( i < 10 ) {
            i = "0" + i;
        }
        return i;
    }

    if(hour > 12) {
        hour = hour - 12;
        timeDisplay.innerHTML = hour + ":" + minute + ((hour === 12) ? " AM" : " PM");
    }
    else {
        timeDisplay.innerHTML = hour + ":" + minute + " AM";
    }

    setTimeout(currentTimeClock, 1000);
}

function setWelcomeText(now, datepickerDatetime) {
    var greetingsText = document.getElementById("greetings");
    var currentHour = now.getHours(),
        datepickerHour = new Date(datepickerDatetime).getHours();

    if(checkCurrentOrCustom(datepickerDatetime)) {
        if(currentHour < 12) {
            greetingsText.innerHTML = "Good Morning."
        } else if(currentHour < 18) {
            greetingsText.innerHTML = "Good Afternoon."
        } else if(currentHour < 23) {
            greetingsText.innerHTML = "Good Evening."
        } else {
            greetingsText.innerHTML = "It's bed time..."
        }
    } else {
        if(datepickerHour < 12) {
            greetingsText.innerHTML = "It's Morning."
        } else if(datepickerHour < 18) {
            greetingsText.innerHTML = "It's Afternoon."
        } else if(datepickerHour < 23) {
            greetingsText.innerHTML = "It's Evening."
        } else {
            greetingsText.innerHTML = "It's bed time..."
        }
    }
}

/*
Function checks if each restaurant item is closing within an hour's time.
If it is, string will be assigned to relevant restaurant card to indicate.
Function also checks if restaurant start and end time is the same, if it's the same, the restaurant is considered
to operate for 24h/7.
 */
function checkShowReopen(datepickerDatetime) {
    $("#restaurants-container").find(".closes-at").each(function (i, obj) {
        var that = $(this),
            currentHour = checkCurrentOrCustom(datepickerDatetime) ?
                new Date().getHours() : new moment(datepickerDatetime, "YYYY-MM-DD HH:mm:ss").hour(),
            currentEndTime = new moment(that.attr("data-current-end-time"), "HH:mm:ss"),
            currentStartTime = new moment(that.attr("data-current-start-time"), "HH:mm:ss"),
            isRestaurantClosing = currentHour >= currentEndTime.hours() - 1,
            endTimeHTML = !currentStartTime.isSame(currentEndTime) ? currentEndTime.format("h:mmA") : "Open 24 hours";

        that.html(
                (isRestaurantClosing ? "<span class=\"text-warning\">Closes soon: </span>" : "Closes ") + endTimeHTML
            );
    });
}

// Initialize handlers when page is loaded.
function initialize() {
    var now = new Date(),
        days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
        months = ['January','February','March','April','May','June','July','August','September','October','November','December'],
        datepickerDatetime = localStorage.getItem("queryDatetime"),
        dayOfWeekDisplay = document.getElementById("day-of-week"),
        currentDateDisplay = document.getElementById("current-date");

    // Fade in each restaurant item with 200ms delay between each item.
    $(".gridbox .restaurant-item-wrapper").each(function() {
        var box = this;
        $("body").queue(function(next) {
            $(box).addClass("fadeIn visible");
            next();
        }).delay(200)
    });

    $('[data-toggle="tooltip"]').tooltip();

    // Handler for producing restaurant's weekly operating hours based on current datetime values.
    $(".current-restaurant-operating-hours").on("click", function () {
        var that = $(this),
            restaurantItem = that.closest(".restaurant-item"),
            restaurantId = restaurantItem.data("current-restaurant-id").length > 0 ?
                restaurantItem.data("current-restaurant-id") : restaurantItem.data("restaurant-id"),
                isCustomDatetime = checkCurrentOrCustom(datepickerDatetime) ? "current/" : "custom/" + queryDatetime.toString(),
            restaurantOperatingHours = restaurantItem.find(".full-restaurant-operating-hours-container");

        var momentDatepickerDatetime = checkCurrentOrCustom(datepickerDatetime) ? "" : new moment(datepickerDatetime).format(dateFormat) + "/";
        var url = "/restaurants/" + isCustomDatetime + restaurantId + "/" +
            momentDatepickerDatetime + "operating_hours";

        function toggleRestaurantItemElements() {
            restaurantOperatingHours.slideToggle();
            that.find(".closes-at").toggle();
            that.find(".closes-at-hide").toggle();
        }

        if(restaurantOperatingHours.css("display") === "none") {
            $.ajax({
                context: this,
                type: "GET",
                url: url, success: function (data) {
                    restaurantOperatingHours.html(data);
                    toggleRestaurantItemElements();
                },
                error: function (err) {
                    console.log(err);
                }
            });
        } else {
            toggleRestaurantItemElements();
        }

        restaurantItem.find(".caret-rotatable")
            .toggleClass('rotated');
    });


    $(".img-menu-btn, .menu-btn").on("click", function () {
        var urlStr = "",
            that = this,
            restaurantItem = $(this).closest(".restaurant-item"),
            restaurantId = restaurantItem.data("current-restaurant-id").length > 0 ?
                restaurantItem.data("current-restaurant-id") : restaurantItem.data("restaurant-id"),
            isCustomDatetime = queryDatetime === "" ? "current/" : "custom/" + queryDatetime.toString();

        // TODO retrieve menus by custom datetime
        $.ajax({
            context: this,
            type: "GET",
            url: "/restaurants/" + isCustomDatetime + restaurantId + "/menus",
            success: function(data) {
                var restaurantMenuModalId = restaurantId + "-modal",
                    modalContainer = document.getElementById("modal-container"),
                    restaurantMenuModal = document.getElementById(restaurantMenuModalId);

                if(modalContainer.contains(restaurantMenuModal) === true) {
                    restaurantMenuModal.remove();
                }

                modalContainer.innerHTML += data;
                // $("#modal-container").find("[data-restaurant-modal='" + restaurantId + "']").modal("show");
                $("#" + restaurantMenuModalId).modal("show");
                $("#centralModalInfo").modal("show");
            },
            error: function (err) {
                console.log("Error");
            }
        });
    });

    // Handler for queue time FAB to trigger modal.
    $(".queue-time-fab").on("click", function () {
        var restaurantItem = $(this).closest(".restaurant-item"),
            restaurantId = restaurantItem.data("current-restaurant-id").length > 0 ?
                restaurantItem.data("current-restaurant-id") : restaurantItem.data("restaurant-id"),
            queueTimeModal = $("#calculate-queue-time-modal");

        queueTimeModal.attr("data-restaurant-id", restaurantId);
        queueTimeModal.find(".modal-restaurant-name").html(
            restaurantItem.find(".restaurant-name").html()
        );
    });

    // Focus on people queueing input field when modal is sown.
    $("#calculate-queue-time-modal").on("shown.bs.modal", function () {
       $("#people-queueing").focus();
    });

    // Handler for Calculate queue time modal form.
    $(document).on("submit", "form#calculate-queue-time", function () {
        var queueTimeModal = $("#calculate-queue-time-modal"),
            restaurantId = queueTimeModal.attr("data-restaurant-id"),
            queueTimeInfoSelector = "#queue-time-info-" + restaurantId,
            restaurantItem = $("#restaurant-item-" + restaurantId);

        queueTimeModal.modal("hide");

        $.ajax({
            context: this,
            type: "GET",
            url: "/restaurants/" + restaurantId + "/" + document.getElementById("people-queueing").value,
            success: function(data) {
                $("#people-queueing").val("");
                if(restaurantItem.has(queueTimeInfoSelector).length === 0) {
                    restaurantItem.append(data);
                } else {
                    $(queueTimeInfoSelector).replaceWith(data);
                }

                $("html, body").animate({
                    scrollTop: $(queueTimeInfoSelector).offset().top - restaurantItem.height()/1.5
                }, 1000);
            },
            error: function (err) {
                alert("Error.");
                console.log(err);
            }
        });
        return false;
    });

    // Handler for individual pagination pages.
    $(".page-number").on("click", function() {
        var pageNumber = $(this).find("span").html();
        toUrl(checkCurrentOrCustom(datepickerDatetime) ?
            pageNumber :
            "custom/" + pageNumber + "/" + datepickerDatetime)
    });

    initializeDatepicker(datepickerDatetime);
    setWelcomeText(now, datepickerDatetime);
    checkShowReopen(datepickerDatetime);
    if(checkCurrentOrCustom(datepickerDatetime)) {
        currentTimeClock();
        dayOfWeekDisplay.innerText = days[now.getDay()];
        currentDateDisplay.innerText = now.getDate() + " " + months[now.getMonth()];
    } else {
        var typedDatePickerDatetime = new Date(datepickerDatetime);
        document.getElementById("tt").innerHTML = moment(datepickerDatetime).format("h:mm A");
        dayOfWeekDisplay.innerText = days[typedDatePickerDatetime.getDay()];
        currentDateDisplay.innerText = typedDatePickerDatetime.getDate() + " " + months[typedDatePickerDatetime.getMonth()];
    }
}

function iteratePage(elementId) {
    var datepickerDatetime = localStorage.getItem("queryDatetime"),
        current_page_number = document.getElementById("restaurant-pagination")
                                        .getAttribute("data-current-page");
    if(elementId === "to-next") {
        current_page_number++;
    } else if(elementId === "to-previous") {
        current_page_number--;
    }

    toUrl(checkCurrentOrCustom(datepickerDatetime) ?
        current_page_number++ : "custom/" + current_page_number++ + "/" + datepickerDatetime)
}

function toUrl(urlToAppend) {
    // window.location.href
    var currentUrl = "http://127.0.0.1:5000/restaurants/" + urlToAppend; // Change if not using local.
    window.location.replace(currentUrl);
}

function initializeDatepicker(datepickerDatetime) {
    var picker = new MaterialDatetimePicker({
        format: dateFormat,
        default: checkCurrentOrCustom(datepickerDatetime) ? moment() : datepickerDatetime
    }).on("submit", function(datetime) {
            var formattedDatetime = datetime.format(dateFormat);
            queryDatetime = formattedDatetime.toString();
            localStorage.setItem("queryDatetime", formattedDatetime);
            toUrl("custom/" + formattedDatetime);
        });

    var el = document.querySelector('.c-datepicker-btn');
    el.addEventListener('click', function() {
        picker.open();
    }, false);
}

function checkCurrentOrCustom(datepickerDatetime) {
    return datepickerDatetime === "" || datepickerDatetime === undefined || datepickerDatetime == null;
}
