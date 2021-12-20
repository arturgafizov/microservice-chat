const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`)

chatSocket.onmessage = receiveMessage

$(function () {
  $('.send_btn').click(sendMessage);
  enter()
});


function newMessage(data) {
  console.log('new_message')
  let currentUser = JSON.parse(localStorage.getItem('user'))
  let currentChat = $('.card-body').attr('chat-id')
  console.log(data.chat_id, currentChat)
  if (data.chat_id === currentChat) {
    let message = ''
    let messageHistory = $('#paginationMessage')
    if (data.author_id === currentUser.id) {
      message = `
      <div class="d-flex justify-content-end mb-4">
        <div class="msg_cotainer_send">
          ${data.content}
          <span class="msg_time_send">${data.date}, Today</span>
        </div>
        <div class="img_cont_msg">
          <img
            src="${data.avatar}" class="rounded-circle user_img_msg">
        </div>
      </div>
      `
    }
    else {
      message = `
      <div class="d-flex justify-content-start mb-4">
        <div class="img_cont_msg">
          <img src="${data.avatar}" class="rounded-circle user_img_msg">
        </div>
        <div class="msg_cotainer">
          ${data.content}
          <span class="msg_time">${data.date}, Today</span>
        </div>
      </div>
      `
    }
    messageHistory.append(message)
  }
  else {
    // todo:сделать жирный шрифт ласт мессадже
  }
}

function changeUserStatus(data) {
   console.log('user_status', data)


}



function receiveMessage(e)   {
  console.log('receiveMessage', e.data)
  let data = JSON.parse(e.data)
  switch (data.command) {
    case('new_message'):
      newMessage(data)
      break;
    case('user_status'):
      changeUserStatus(data)
      break
  }


}

function enter () {
    $("#userMessage").keyup(function(event) {
        if (event.keyCode === 13 && event.ctrlKey || event.keyCode === 13) {
            $(".send_btn").click();
        }
    });
}

function sendMessage(e) {
    e.preventDefault();
    let message = $('#userMessage').val()

    let chatId = ($('.card-body').val('chat-id')[0]).getAttribute('chat-id')
    let data = {
      'command': 'new_message',
      'message': message,
      'chat_id': chatId,
    }

    console.log(data)
    chatSocket.send(JSON.stringify(data))
    $('#userMessage').val('')
}
