$(document).ready(function() {
  let player = {{ current_user.username }};
  let url = `https://api.hotslogs.com/Public/Players/1/${player}`

  $.get(url, function (data) {
      console.log((data));

      for (let row of data['LeaderboardRankings']) {
          if (row['LeagueRank'] !== null) {
          $('#myTable > tbody:last-child').append(`<tr>${row['GameMode']}<tr>test</tr><tr>test</tr><tr>test</tr>`)
          }
      }
  });
 });