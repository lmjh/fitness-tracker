/* jshint esversion: 8, jquery: true */
$(document).ready(function () {
  // Initialise Materialize components
  $('.sidenav').sidenav({
    edge: "right"
  });
  $('.collapsible').collapsible();
  $('select').formSelect();
  $('.datepicker').datepicker({
    format: "dd/mm/yy"
  });
  $('.timepicker').timepicker({
    twelveHour: false
  });
  $('.modal').modal();
  $('.tooltipped').tooltip();

  // Materialize Validation function by TravelTimN:
  // https://github.com/Code-Institute-Solutions/TaskManagerAuth/blob/main/04-AddingATask-WritingToTheDatabase/02-materialize-select-validation/static/js/script.js
  // Slightly adapted by using add/remove class instead of directly applying cSS to the elements
  validateMaterializeSelect();

  function validateMaterializeSelect() {
    if ($("select.validate").prop("required")) {
      $("select.validate").css({
        "display": "block",
        "height": "0",
        "padding": "0",
        "width": "0",
        "position": "absolute"
      });
    }
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
      $(this).parent(".select-wrapper").on("change", function () {
        if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
          $(this).children("input").addClass("select-valid");
          $(this).children("input").removeClass("select-invalid");
        }
      });
    }).on("click", function () {
      if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
        $(this).parent(".select-wrapper").children("input").addClass("select-valid");
        $(this).parent(".select-wrapper").children("input").removeClass("select-invalid");
      } else {
        $(".select-wrapper input.select-dropdown").on("focusout", function () {
          if ($(this).parent(".select-wrapper").children("select").prop("required")) {
            if (!$(this).hasClass("select-valid")) {
              $(this).parent(".select-wrapper").children("input").addClass("select-invalid");
              $(this).parent(".select-wrapper").children("input").removeClass("select-valid");
            }
          }
        });
      }
    });
  }
});