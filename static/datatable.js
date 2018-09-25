// https://www.datatables.net/examples/basic_init/multiple_tables.html
// CAN ROLL ALL THIS INTO ONE CLASS INSTEAD OF MULTIPLE IDS
// ISSUE WAS CACHED JS FILE
$(document).ready(function () {
  $('.display').DataTable({
    'order': [[1, 'desc']]
  });
});
$(window).scroll(function () {
  var scroll = $(window).scrollTop();

  if (scroll >= 300) {
    $('#stickyheader').addClass('isStuck',);
    $('#stickyheader').addClass('container-fluid');
    $('#stickyheader').removeClass('container');
  } else {
    $('#stickyheader').removeClass('isStuck');
    $('#stickyheader').addClass('container');
    $('#stickyheader').removeClass('container-fluid');
  }
});
