<!DOCTYPE HTML>
<html>
  <head>
    <title>Personalized Marketing</title>

    <script src="./lib/js/jquery-2.1.3.min.js"></script>
    <script src="./lib/js/jquery-ui/jquery-ui.min.js"></script>
    <script src="./lib/js/jquery.cookie.js"></script>
        
  </head>

  <body>
    <script>
  window.fbAsyncInit = function() {
    FB.init({
      appId            : '118340725490952',
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

        var i=0;

        //$("table").each(function(){
        for (i=0;i<response.data.length;i++){
          $("tr:nth-child("+(i+1)+") td:nth-child(1)").html(i);
          $("tr:nth-child("+(i+1)+") td:nth-child(2)").html(response.data[i].id);
          $("tr:nth-child("+(i+1)+") td:nth-child(3)").html(response.data[i].name);
          //i++;
        }
        //});

        /*$("table tr td:nth-child(2)").each(function(){
          $(this).html(response.data[i].name);
          i++;
        });

        i=0;

        $("table tr td:nth-child(3)").each(function(){
          $(this).html(response.data[i].id);
          i++;
        });

        i=0;

        $("table tr td:nth-child(1)").each(function(){
          $(this).html(i);
          i++;
        });*/

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
        /*categories[i] = category;
        i++;

        if (i==24){
          i=0;*/
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
        
        <script>
        window.twttr = (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0],
          t = window.twttr || {};
        if (d.getElementById(id)) return t;
        js = d.createElement(s);
        js.id = id;
        js.src = "https://platform.twitter.com/widgets.js";
        fjs.parentNode.insertBefore(js, fjs);

        t._e = [];
        t.ready = function(f) {
          t._e.push(f);
        };

        return t;
        }(document, "script", "twitter-wjs"));
        </script>
        
        <script>
      function myTwitter(){
              $.ajax({
                  type: "POST",
                  url : "https://api.twitter.com/oauth/request_token",
                    dataType : "json",
                    success : function(data)
                    {
                        console.log(data);
                    },
                    error : function()
                    {
                        alert("Failure!");
                    }

                    /*url : "http://api.twitter.com/1/users/show.json?screen_name=giulioCardz",
                    dataType : "jsonp",
                    success : function(data)
                    {
                        console.log(data);
                    },
                    error : function()
                    {
                        alert("Failure!");
                    },*/

                });
      }
    </script>
        
        <script>
          function downloadPage(){
            
            $.ajaxPrefilter( function (options) {
              if (options.crossDomain && jQuery.support.cors) {
                var http = (window.location.protocol === 'http:' ? 'http:' : 'https:');
                options.url = http + '//cors-anywhere.herokuapp.com/' + options.url;
                //options.url = "http://cors.corsproxy.io/url=" + options.url;
              }
            });
            
            $.ajax({
              type:"GET",
                access_token:"EAABroVjnxQgBAE7rP1mUIPKQ31qMkf2UZA8FfZBAUFm6WEab3GbZAUf55VISIhWYhlZCJ9AMP0oq6HAcNecqBZA2ZAPjA6wMn4ZCevrUwxSHkI4yr3NZC8co6Dz3aWKvhBdBS7OIUZCluNWPvY6XsIUz0HjZBoZAhkJZA7zZCWF8x3BYXkn6OYBVwNpFboZBnQZACJekoZAriqKnMOxXTQZDZD",
                url:"https://www.facebook.com/profile.php?id=100020334273014",
                success: function (response) {
                    console.log(response);
                },
                failure: function() {console.log("fag");},
            });

            /*$.get(
                //'http://en.wikipedia.org/wiki/Cross-origin_resource_sharing',
                'https://www.facebook.com/giuse.rizzo',
                function (response) {
                    console.log(response);
                    //$("#viewer").html(response);
            });*/
            
            
            
            //alert("lol");
              /*$.ajax({
                  type:"GET",
                  url:"http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20htmlstring%20where%20url%3D'https://www.facebook.com/giuse.rizzo'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys",
                    dataType:"json",
                    success : function(data)
                    {
                      console.log("SUCCESS !!!!");
                        console.log(data);
                    },
                    error : function(data)
                    {
                        //alert("Failure!");
                        console.log("FAILURE !!!!");
                        console.log(data);
                    }
                });*/
            };
        </script>

    <!--<div class="fb-login-button" data-max-rows="1" data-size="large" data-button-type="continue_with" data-show-faces="false" data-auto-logout-link="false" data-use-continue-as="false"></div>
-->
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
        <br>
        <div id="lol7"><button onclick="downloadPage()">download facebook page</button></div>
        <br>
        <br>
        
        <form method="GET" action="twitter_login.php">
        <input type="submit" value="twitter login">
        <!--<button onclick="myTwitter()">test Twitter</button>-->
        </form>
        
        
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
        
        <?php
        //require_once 'Facebook\FacebookRequest.php';
          /*include  'Facebook/autoload.php';
        
          $fb = new Facebook/Facebook([
              'app_id' => '196245240908861',
              'app_secret' => 'a3c8ff54e37577ccd17ec17b87ba9942',
              'default_graph_version' => 'v2.4',
            ]);
            
            $request = new FacebookRequest(
              $session,
              'GET',
              '/me'
            );
            $response = $request->execute();
$graphObject = $response->getGraphObject();*/
            
            //$fb->setAccessToken($initMe["accessToken"]);
      //$response = $fb->get('/me?locale=en_US&fields=name,email');
            
            //$user = $fb->getUser();
            
          /*$json = $facebook->api('/me');            
            $first = $json['first_name']; // gets first name
      $last = $json['last_name'];            
            echo 'il tuo nome è '.$first.'<br>';
            echo 'il tuo cognome è '.$last.'<br>';*/
        ?>

  </body>
</html>
