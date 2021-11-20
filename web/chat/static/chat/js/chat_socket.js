const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`)

chatSocket.onmessage = receiveMessage

$(function () {
  $('.send_btn').click(sendMessage);
});

function receiveMessage(e)   {
  console.log('receiveMessage', e.data)
  let data = JSON.parse(e.data)
}


function sendMessage(e) {
    e.preventDefault();
    console.log('click')
    let message = $('#userMessage').val()
    let chatId = ($('.card-body').val('chat-id')[0]).getAttribute('chat-id')
    let data = {
      'command': 'new_message',
      'message': message,
      'chat_id': chatId,
    }

    console.log(data)
    chatSocket.send(JSON.stringify(data))
}
