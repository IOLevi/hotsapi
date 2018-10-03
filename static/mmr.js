$(document).ready(function() {
  let player = $('#player').data('username');
  let url = `https://api.hotslogs.com/Public/Players/1/${player}`

  $.get(url, function (data) {
    console.log((data));

    $('#qm').html(data['LeaderboardRankings'][0]['CurrentMMR']);
  });
});