console.log('chat')

$(function () {
  getChat()
  $('.chatItem').click(makeActiveChat)
});

function getChat() {
    let pagination = $('#paginationContact')

    $.ajax({
      url: pagination.attr('data-href'),
      type: 'GET',
      success: function (data){
          console.log('success', data)
          renderChatList(data, pagination)
      },
      error: function (data){
          console.log('error', data)
      }
  })
}

function renderChatList(data, pagination){
    $.each(data.results, function(i){
      let block = `
          <li class="chatItem">
            <div class="d-flex bd-highlight">
              <div class="img_cont">
                <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img">
                <span class="online_icon"></span>
              </div>
              <div class="user_info">
                <span>Khalid</span>
                <p>Kalid is online</p>
              </div>
            </div>
          </li>
      `
      pagination.append(block)
    })
  $('.chatItem').click(makeActiveChat)
}

function makeActiveChat() {
  console.log('click')
  $('.active').removeClass('active')
  $(this).addClass('active')
}
