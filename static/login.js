const clientId = '1011824361501-id0m8g61iu283r7mbd086t7c0d0glmdc.apps.googleusercontent.com';
const googleOauthUrl = 'https://accounts.google.com/o/oauth2/auth';
const redirectUri = 'http://localhost:5000/user/gconnect';
const scopes = [
  'https://www.googleapis.com/auth/userinfo.profile',
  'https://www.googleapis.com/auth/plus.login',
  'openid',
  'email',
  'https://www.googleapis.com/auth/plus.me'
];

// function to make a redirect to the google login url
function login(state) {

    const joinedScopes = scopes.join('+');
    
    const googleUrl = googleOauthUrl +
      '?client_id=' + clientId +
      '&redirect_uri=' + redirectUri +
      //'accesstype=offline' &
      '&scope=' + joinedScopes +
      '&response_type=code' +
      '&state=' + state;

      window.location = googleUrl;
}

// function to send an ajax request to the server to deauthenticacte the current user
function logout(state, url) {
    const logoutUrl = url + '?session_token=' + state;
    sendAjaxPOSTRequest(logoutUrl).addEventListener('load', function(event) {
        window.location.reload();
    });
}