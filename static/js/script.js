$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('select').formSelect();
    today = new Date();
    $('.datepicker').datepicker({format: "dd mmmm yy", defaultDate: today, setDefaultDate: true});
    $('.timepicker').timepicker({defaultTime: "now"});
  });