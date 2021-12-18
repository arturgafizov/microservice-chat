console.log('chat')

$(function () {
  getChat()
  getMessage()

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

function getMessage() {
    let pagination = $('#paginationMessage')

    $.ajax({
      url: pagination.attr('data-href'),
      type: 'GET',
      success: function (data){
          console.log('success', data)
          userMessageRender(data, pagination)
          requestedMessageNewPage = false
      },
      error: function (data){
          console.log('error', data)
      }
  })
}


function renderChatList(data, pagination){
    pagination.attr('data-href', data.next)
    $.each(data.results, function(i){
      console.log(data.results[i])
      let contactUser = null
      for (let j of data.results[i].user_chat) {
        if (j.id) contactUser = j
      }
      // console.log(contactUser)
      let block = `
          <li class="chatItem" id="${data.results[i].id}">
            <div class="d-flex bd-highlight">
              <div class="img_cont" >
                <img src="${contactUser.avatar_url}" class="rounded-circle user_img">
                <span class="online_icon"></span>
              </div>
              <div class="user_info">
                <span> ${contactUser.full_name}</span>
                <p>last user visited / ${data.results[i].last_message}</p>
              </div>
            </div>
          </li>
      `
      pagination.append(block)
    })
  $('.chatItem').click(makeActiveChat)
}

function formaDate(messageDate) {
  let currentDate = new Date()

  // console.log(date.getDate())
  // console.log(Date.now()/(1000*3600*24)/365)
  let dateDiff = currentDate.getDate() - date.getDate()
  // console.log(dateDiff)
  if (dateDiff === 1) {
    console.log('Today')
    return messageDate
  }
  if (dateDiff === 2) {
    console.log('Yesterday')

  }
  else {
    date.getDate()
  }
}


function userMessageRender(data, pagination) {
    pagination.attr('data-href', data.next)
    $.each(data.results, function (i){
      console.log('DATA', data.results[i])
      let contactUser = data.results[i].author

      let currentUser = JSON.parse(localStorage.getItem('user'))
      let message = ''
      let date = new Date(data.results[i].date)
      // console.log(date.getDay(), date.getHours(),date.getMinutes(), date.getSeconds())
      if (data.results[i].author_id === currentUser.id) {
          message = `
            <div class="d-flex justify-content-end mb-4">
              <div class="msg_cotainer_send">
                ${data.results[i].content}
                <span class="msg_time_send">${date.toLocaleTimeString()}, Day ${formaToday(date)}</span>
              </div>
              <div class="img_cont_msg">
                <img
                  src="${currentUser.avatar_url}"
                  class="rounded-circle user_img_msg">
              </div>
            </div>
           `
      }
      else {
          message = `
          <div class="d-flex justify-content-start mb-4">
            <div class="img_cont_msg">
              <img src="${contactUser.avatar_url}" class="rounded-circle user_img_msg">
            </div>
            <div class="msg_cotainer">
              ${data.results[i].content}
              <span class="msg_time">${formaDate(date)}</span>
            </div>
          </div>
            `
       }
      pagination.prepend(message)
    })
    $('.msg_card_body').scrollTop($('.msg_card_body').prop('scrollHeight'))
}


function makeActiveChat() {
  let cardBody = $('.card-body') //
  if (cardBody.attr('chat-id') === $(this).attr('id')) return
  let messageApi = '/chat/message/' + $(this).attr('id') + '/'
  cardBody.attr('chat-id', $(this).attr('id'))
  cardBody.attr('data-href', messageApi)
  console.log('click')
  $('.active').removeClass('active')
  $('.msg_card_body').empty()
  $(this).addClass('active')


  getMessage()

}


let requestedNewPage = false
let requestedMessageNewPage = false


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


$('#paginationMessage').scroll(function () {
// End of the document reached?
    let pagination = $(this)
    // console.log($(this).prop('scrollHeight') - $(this).innerHeight(), $(this).scrollTop() )
    if ($(this).scrollTop() <= 30 && !requestedMessageNewPage) {
        let nextUrl = pagination.attr('data-href')
        // console.log('here')
        // console.log(nextUrl)

        if (nextUrl) {
            requestedMessageNewPage = true
            getMessage()


        }
    }
});
