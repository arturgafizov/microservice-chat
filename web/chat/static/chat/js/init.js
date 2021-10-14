console.log('init')

$(function () {
  getJwt()


});

function getJwt() {
    console.log('jwt')
    let paramsString = window.location.search
    console.log(paramsString)
    let searchParams = new URLSearchParams(paramsString);
    let jwt = searchParams.get("jwt")
    let data = {
      'jwt': jwt
    }
    console.log(jwt);
    $.ajax({
      url: '/chat/init/',
      type: 'POST',
      data: data,
      success: function (data){
          console.log('success', data)

      },
      error: function (data){
          console.log('error', data)
      }
  })
}
