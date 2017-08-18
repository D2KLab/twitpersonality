<!DOCTYPE HTML>
<html>
	<head>
		<title>FB personality</title>

		<script src="./lib/js/jquery-2.1.3.min.js"></script>
		<script src="./lib/js/jquery-ui/jquery-ui.min.js"></script>
		<script src="./lib/js/jquery.cookie.js"></script>
        
	</head>

	<body>

    <script>
      window.fbAsyncInit = function() {
        FB.init({
          appId            : '196245240908861',
          autoLogAppEvents : true,
          xfbml            : true,
          version          : 'v2.10'
        });
        FB.AppEvents.logPageView();
      };

      (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));
    </script>

    <script>
      function acctok(){
      FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
          accessToken = response.authResponse.accessToken;
          console.log('access token: '+accessToken);
          $("#tok").text("il tuo access token è "+accessToken);
          $("#tok").show();
        } 
      } );
      }
    </script>

    <script>
      function permissions(){
      FB.api(
          "/me/permissions",
          function (response) {
            if (response && !response.error) {
              console.log(response);
            }
          }
      );
      }
    </script>

    <script>
      function myLogin(){
      FB.login(function(response) {
        console.log(response);
      }, {scope: 'email,user_likes,user_friends,user_birthday'});
      }
    </script>

    <script>
      function likes(){
      FB.api(
          "/me/likes",
          function (response) {
            if (response && !response.error) {
              console.log(response);

              for (var j=0;j<response.data.length;j++){
                fillCategories(response.data[j].id, j);
              }

              for (i=0;i<response.data.length;i++){
                $("tr:nth-child("+(i+1)+") td:nth-child(1)").html(i);
                $("tr:nth-child("+(i+1)+") td:nth-child(2)").html(response.data[i].id);
                $("tr:nth-child("+(i+1)+") td:nth-child(3)").html(response.data[i].name);
              }

              $("#likes").show();
            }
          }
      );
      }

      function fillCategories(pageID, number){

        var categories = [];

        FB.api(
          "/"+pageID,
          {fields: 'category'},
          function(response2){
            if (response2 && !response2.error) {
              console.log(response2);
              category = response2.category;

                i=0;
                $("table tr td:nth-child(4)").each(function(){
                  if (i==number){
                    $(this).html(category);
                  }
                  i++;
                });
            }
          }
        );

      }
    </script>

    <script>
      function myFunc(){
      FB.api(
          "/me",
          {fields: 'first_name, last_name, gender, age_range, email, birthday'},
          function (response) {
            if (response && !response.error) {
              /* handle the result */
              console.log(response);

              $("#name").text("name: " + response.first_name);
              $("#surname").text("surname: " + response.last_name);
              $("#age_range").text("age range: " + response.age_range.min + " - " + response.age_range.max);
              $("#birthday").text("birthday: " + response.birthday)
              $("#gender").text("gender: " + response.gender);
              $("#email").text("email: " + response.email);
              $("#results").show();
            }
            else {
            console.log(response);
            }
          }
      );}
    </script>

    <script>
    	// Only works after `FB.init` is called
    	function myFacebookPost() {
    	  FB.login(function(){
    	  	FB.api('/me/feed', 'post', {message: 'Hello, world!'});
    	  }, {scope: 'publish_actions'});
    	}
    </script>

    <div id="lol1"><button onclick="myLogin()">login</button></div>
    <br>
    <div id="lol2"><button onclick="acctok()">get access token</button></div>
    <br>
    <div id="asdasd"><button onclick="myFacebookPost()">post something</button></div>        
    <br>
    <div id="lol3"><button onclick="myFunc()">profile information</button></div>
    <br>
    <div id="lol4"><button onclick="permissions()">my permissions</button></div>
    <br>
    <div id="lol5"><button onclick="likes()">my likes</button></div>
    <br>
    <br>
    <div id="tok" hidden></div>
    <div id="fbid" hidden></div>
    <div id="res" hidden></div>
    <div id="res2" hidden></div>

    <div id="results" hidden>
      <p id="name">name: </p>
      <p id="surname">surname: </p>
      <p id="age_range">age range: </p>
      <p id="birthday">birthday: </p>
      <p id="gender">gender: </p>
      <p id="email">email: </p>
    </div>

    <div id="likes" hidden>
      <table>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
      </table>
    </div>

    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <div
      class="fb-like"
      data-share="true"
      data-width="450"
      data-show-faces="true">
    </div>

	</body>
</html>