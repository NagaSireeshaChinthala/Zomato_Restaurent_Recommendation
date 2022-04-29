var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    $('<div class="message new"><figure class="avatar"><img src="/static/robo2.jpg" /></figure>' + 'Hi, I am your restaurent bot.' + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function() {
    $('<div class="message loading new"><figure class="avatar"><img src="/static/robo2.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();


    fetch(`${window.origin}/entry`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(msg),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function(response) {
      if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function(data) {
        console.log(data);

        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="/static/robo2.jpg" /> </figure>' + data.name  + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();


      });
    })
    .catch(function(error) {
      console.log("Fetch error: " + error);
   });

  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

var Fake = [
  'Hi im your chatbot ',
  'please enter your name ',
  'Please Enter Your age',
  'good.....What is your comfortable level for investment loss (in %) <input type="range" value="50" min="0" max="100" step="10" />',
  'we are Predicting... <div class="loading-img"><img src="5.png"  alt=""/></div>',
  'great.. do you want to predict another? <button class="buttonx sound-on-click">Yes</button> <button class="buttony sound-on-click">No</button> ',
  'Bye',
  ':)'
]

function fakeMessage() {
  msg = $('.message-input').val()
  if (msg != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="/static/robo2.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    fetch(`${window.origin}/entry`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(msg),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function(response) {
      if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function(data) {
        console.log(data);
        $('<div class="message new"><figure class="avatar"><img src="/static/robo2.jpg" /></figure>' + data.name + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();


      });
    })
    .catch(function(error) {
      console.log("Fetch error: " + error);
   });

    i++;
  }, 1000 + (Math.random() * 20) * 100);

}