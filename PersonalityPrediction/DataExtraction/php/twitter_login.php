<?php
    session_start();
    
    require "twitteroauth/autoload.php";
    use Abraham\TwitterOAuth\TwitterOAuth;
    
    //Define app key and app secret
    define('APP_KEY','Bo0Usm7MbQLJGTUv3jAuwY1qz');
    define('APP_SECRET','hx0gsX49KIDsm1MgWFuuYOV1zrR06Tcz5r06RmMxn4SsR41dFr');
    
    //Define callback URL
    //$auth_page='http://'.$_SERVER["HTTP_HOST"].$_SERVER["PHP_SELF"];
    $callback='http://personalizedmarketing.altervista.org/twitter.php';
    
    //Start the oauth process
    if(!isset($_SESSION['oauth_token'])){
    
    	/*$request_token = [];
        $request_token['oauth_token'] = $_SESSION['oauth_token'];
        $request_token['oauth_token_secret'] = $_SESSION['oauth_token_secret'];
        $connection = new TwitterOAuth(APP_KEY, APP_SECRET);
    	$request_token = $connection->oauth('oauth/request_token', array('oauth_callback' => $callback));
        var_dump($connection);*/
    
        $tweet = new TwitterOAuth(APP_KEY, APP_SECRET);
        $request_token = $tweet->oauth('oauth/request_token', ['oauth_callback' => $callback]);
        
        //$request_token["oauth_callback_confirmed"] must be true
        
        $_SESSION["oauth_token"]=$request_token["oauth_token"];
        $_SESSION["oauth_token_secret"]=$request_token["oauth_token_secret"];
        
        if($tweet->getLastHttpCode()==200){
            $url = $tweet->url(
                'oauth/authenticate', [
                    'oauth_token' => $request_token['oauth_token']
                ]
            );
            header("Location:".$url);
        }else{
            die("Error on the login_twitter page");
        }
    }
    else{
        if(!empty($_GET["oauth_verifier"])&&isset($_SESSION['oauth_token'])&&!empty($_SESSION["oauth_token"])&&!empty($_SESSION["oauth_token_secret"])){
            $tweet=new TwitterOAuth(APP_KEY,APP_SECRET,$_SESSION["oauth_token"],$_SESSION["oauth_token_secret"]);
            
            $access_token=$tweet->getAccessToken($_GET['oauth_verifier']);
            // Save it in a session var 
            $_SESSION['access_token'] = $access_token; 
            
            if($_SESSION["access_token"]!=null){
                $_SESSION["twitter_token"]=$access_token["oauth_token"];
                $_SESSION["twitter_secret"]=$access_token["oauth_token_secret"];
                header("location:".$callback);
            }
        }else{
            echo 'Error while authenticatng';
            unset($_SESSION['oauth_token']);
        }
    }
