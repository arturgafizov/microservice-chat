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
    let user_id = searchParams.get('user_id')

    let data = {
      'jwt': jwt,
      'user_id': user_id,
    }
    console.log(jwt);
    $.ajax({
      url: '/chat/init/',
      type: 'POST',
      data: data,
      success: function (data){
          console.log('success', data)
          localStorage.setItem('user', JSON.stringify(data))
          window.location.replace('/')
      },
      error: function (data){
          console.log('error', data)
      }
  })
}

