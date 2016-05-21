function graph(data_for_graph, x) {
  if ($('#biorythms_chart').css('display') == 'none') {
    return;
  }
  $('#biorythms_chart').addClass("loading");
  new Morris.Line({
    element: 'biorythms_chart',
    data: data_for_graph,
    dateFormat: function (x) {
        function addZero(i) {
            return (i < 10)? "0" + i: i;
        }
        function week_day(x) {
          switch(x) {
              case 0:r = "Воскресенье";break;
              case 1:r = "Понедельник";break;
              case 2:r = "Вторник";break;
              case 3:r = "Среда";break;
              case 4:r = "Четверг";break;
              case 5:r = "Пятница";break;
              case 6:r = "Суббота";break;
          }
          return r;
        }
      var day = new Date(x);
      return (
          week_day(day.getDay())+' ' +
          addZero(day.getDate()) + '.' +
          addZero(day.getMonth()+1) + '.' +
          day.getFullYear()
      );
  },
  xLabelFormat: function (x) {
      function addZero(i) {
          return (i < 10)? "0" + i: i;
      }
      var day = new Date(x);
      return addZero(day.getDate())+'.'+addZero(day.getMonth()+1);
  },
  xkey: 'day',
  ykeys: ['fiz', 'emo', 'smart'],
  labels: ['физический', 'эмоциональный', 'интеллектуальный'],
  hideHover: 'auto',
  events: function(data_for_graph) {
    first_day = data_for_graph[0].day
    last_day = data_for_graph.slice(-1)[0].day
    if (today_date > first_day && today_date < last_day) {
      dates = [today_date]
    }
    else {
      dates = []
    }
    if (current_date != today_date) {
      dates.push(current_date);
    };
    return dates
  }(data_for_graph),
  pointSize:2,
  lineColors: ['#e67869','#3b9647', '#193020'],
  eventLineColors: function(data_for_graph) {
    first_day = data_for_graph[0].day
    last_day = data_for_graph.slice(-1)[0].day
    if (today_date > first_day && today_date < last_day) {
        return ['#193020', '#f37019'];
    } else {
        return ['#f37019'];
    }

  }(data_for_graph),
  eventStrokeWidth: 2,
});
  $('#biorythms_chart').removeClass("loading");
}

var click = false
function bio_ajax(){
  $('.get_bio_data').click(function() {
    if (window.click) {return false;}
    window.click = true;
    
    day = $(this).attr('day');
    $('#biorythms_chart').html('');
    $.get(url_ajax_get_data+'?day='+day, function(data) {
        $('.bio_info').html(data);
        window.click = false;
        
    });
    return false;

});
}

graph(biorythm_data);

bio_ajax();
