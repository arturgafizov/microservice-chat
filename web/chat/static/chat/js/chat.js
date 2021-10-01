console.log('chat')

$(function () {
  getChat()
  $('.chatItem').click(makeActiveChat)
});

function getChat() {
    let pagination = $('#paginationContact')
    let chat_id = pagination.id
    console.log(chat_id)
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
// data-id='${pagination[i].id}'
function renderChatList(data, pagination){
    pagination.attr('data-href', data.next)
    $.each(data.results, function(i){

      let block = `
          <li class="chatItem" id="${data.results[i].id}">
            <div class="d-flex bd-highlight">
              <div class="img_cont" >
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
  if ($('.card-body').attr('chat-id') === $(this).attr('id')) return

  $('.card-body').attr('chat-id', $(this).attr('id'))
  console.log('click')
  $('.active').removeClass('active')
  $(this).addClass('active')

}


let requestedNewPage = false

$('#chatListPagination').scroll(function () {
// End of the document reached?
    let pagination = $('#paginationContact')

    // console.log($(this).prop('scrollHeight') - $(this).innerHeight(), $(this).scrollTop() )
    if ($(this).prop('scrollHeight') -  $(this).innerHeight() <= $(this).scrollTop() && !requestedNewPage) {
        requestedNewPage = true
        console.log('here')
        let nextUrl = pagination.attr('data-href')
        if (nextUrl) {
            requestedNewPage = false
            getChat()
        }
    }
});
