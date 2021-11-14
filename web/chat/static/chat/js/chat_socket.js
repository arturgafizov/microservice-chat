const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`)

chatSocket.onmessage = receiveMessage

$(function () {
  $('.send_btn').click(sendMessage);
});

function receiveMessage(e)   {
  console.log(e.data)
}

function sendMessage(e) {
    e.preventDefault();
    console.log('click')

}
