<?php
    
    require "twitteroauth/autoload.php";
    use Abraham\TwitterOAuth\TwitterOAuth;
    session_start();
    
    $_SESSION["oauth_verifier"] = $_GET["oauth_verifier"];
    
    $twitter = new TwitterOAuth(
        "Bo0Usm7MbQLJGTUv3jAuwY1qz",
        "hx0gsX49KIDsm1MgWFuuYOV1zrR06Tcz5r06RmMxn4SsR41dFr",
        $token['oauth_token'],
        $token['oauth_token_secret']
    );
    
    if(isset($_POST["twitter_handle"])){
        $handle = $_POST["twitter_handle"];
        if (substr($handle,0,5) == "https" || substr($handle,0,5) == "http"){
            $handle = explode("/", $handle, 4)[3];
        }
        else if (substr($handle,0,1) == "@"){
            $handle = substr($handle, 1, strlen($handle)-1);
        }
        echo "twitter handle: ".$handle."<br><br>";
        
        $ids_path = "./Data/".$handle."/".$handle."_ids.txt";
        $names_path = "./Data/".$handle."/".$handle."_names.txt";
        $tweets_path = "./Data/".$handle."/".$handle."_tweets.txt";
        
        $data = $twitter->get(
            "users/show", [screen_name => $handle]
        );
        
        if (!file_exists("Data/".$handle."/")){
            mkdir("Data/".$handle."/", 0700);
        }
        if (file_exists($ids_path) && filesize($ids_path) > 0) {
        	echo "Reading IDs from file...<br>";
            $friends_ids = include $ids_path;  
        }
        else {
        	echo "Reading IDs from Twitter...<br>";
            $cursor = -1;
            $friends_ids = [];
            do {
                $response = $twitter->get(
                    "friends/ids", [screen_name => $handle, cursor => $cursor]
                );
                if (count($response->errors) > 0){var_dump($response);echo'<br>';break;}
                $friends_ids = array_merge($friends_ids, $response->ids);
                $cursor = $response->next_cursor;
            } while ($cursor != 0);
            file_put_contents($ids_path,  '<?php return ' . var_export($friends_ids, true) . ';');
            echo "IDs written in file<br>";
        }
        if (file_exists($names_path) && filesize($names_path) > 0) {
        	echo "Reading names from file...<br>";
            $friends_names = include $names_path;
        }
        else {
        	echo "Reading names from Twitter...<br>";
            $friends_names = [];
            for ($i=0;$i<count($friends_ids);$i++){
              $response = $twitter->get(
                "users/show", [user_id => $friends_ids[$i]]
              );
              $friends_names[$i] = $response->name;
            }
            file_put_contents($names_path,  '<?php return ' . var_export($friends_names, true) . ';');
            echo "Names written in file<br>";
        }
        //}
        if (file_exists($tweets_path) && filesize($tweets_path) > 0) {
        	echo "Reading tweets from file...<br>";
            $tweets = include $tweets_path;
        }
        else {
        	echo "Reading tweets from Twitter...<br>";
            $tweets=[];
            $response = $twitter->get(
                "statuses/user_timeline", [screen_name => $handle, count => 200]
            );
            for ($i=0;$i<count($response);$i++){
            	$tweets[$i] = $response[$i]->text;
            }
            file_put_contents($tweets_path,  '<?php return ' . var_export($tweets, true) . ';');
            echo "Tweets written in file<br>";
        }        
    }
    
    
    
    /*$connection = new TwitterOAuth(
        "Bo0Usm7MbQLJGTUv3jAuwY1qz",
        "hx0gsX49KIDsm1MgWFuuYOV1zrR06Tcz5r06RmMxn4SsR41dFr",
        $_SESSION['oauth_token'],
        $_SESSION['oauth_token_secret']
    );
    
    $token = $connection->oauth(
        'oauth/access_token', [
            'oauth_verifier' => $_GET["oauth_verifier"]
        ]
    );*/
?>

<!DOCTYPE HTML>
<html>
  <head>
    <title>Personalized Marketing</title>

    <script src="./lib/js/jquery-2.1.3.min.js"></script>
    <script src="./lib/js/jquery-ui/jquery-ui.min.js"></script>
    <script src="./lib/js/jquery.cookie.js"></script>
        
  </head>

  <body>
        <form method="POST">
            <p>Enter full path (https://www.twitter.com/username) or just the username (@username)</p>
            <p><input type="text" name="twitter_handle" placeholder="twitter handle"></p>
            <p><button type="submit" formaction="twitter.php">search</button></p>
        </form>
        
        <?php
            if (isset($_POST["twitter_handle"])){
                if (sizeof($data->errors) == 1){
                    echo "Error occurred";
                    var_dump($data);
                }
                else{
                    echo "Displaying information about user @".$handle."<br><br>";
                    if ($data->default_profile_image != 1){echo"<img src=".$data->profile_image_url."></img><br><br>";}
                    echo"<table>";
                    echo"<tr><td>name</td><td>".$data->name."</td></tr>";
                    echo"<tr><td>account creation</td><td>".$data->created_at."</td></tr>";
                    echo"<tr><td>default_profile</td><td>".(boolval($data->default_profile) ? 'true' : 'false')."</td></tr>";
                    echo"<tr><td>default_profile_image</td><td>".(boolval($data->default_profile_image) ? 'true' : 'false')."</td></tr>";
                    echo"<tr><td>description</td><td>".$data->description."</td></tr>";
                    echo"<tr><td>favourites_count</td><td>".$data->favourites_count."</td></tr>";
                    echo"<tr><td>followers_count</td><td>".$data->followers_count."</td></tr>";
                    echo"<tr><td>listed_count</td><td>".$data->listed_count."</td></tr>";
                    echo"<tr><td>friends_count</td><td>".$data->friends_count."</td></tr>";
                    echo"<tr><td>geo_enabled</td><td>".(boolval($data->geo_enabled) ? 'true' : 'false')."</td></tr>";
                    echo"<tr><td>id</td><td>".$data->id."</td></tr>";
                    echo"<tr><td>lang</td><td>".$data->lang."</td></tr>";
                    echo"<tr><td>location</td><td>".$data->location."</td></tr>";
                    if ($data->default_profile_image != 1){echo"<tr><td>profile_image_url</td><td>".$data->profile_image_url."</td></tr>";}
                    if ($data->default_profile != 1){echo"<tr><td>profile_background_image_url</td><td>".$data->profile_background_image_url."</td></tr>";}
                    echo"<tr><td>profile_banner_url</td><td>".$data->profile_banner_url."</td></tr>";
                    echo"<tr><td>protected</td><td>".(boolval($data->protected) ? 'true' : 'false')."</td></tr>";
                    echo"<tr><td>screen_name</td><td>".$data->screen_name."</td></tr>";
                    echo"<tr><td>statuses_count</td><td>".$data->statuses_count."</td></tr>";
                    echo"<tr><td>time_zone</td><td>".$data->time_zone."</td></tr>";
                    echo"<tr><td>url</td><td>".$data->url."</td></tr>";
                    echo"<tr><td>verified</td><td>".(boolval($data->verified) ? 'true' : 'false')."</td></tr>";
                    echo"</table>";
                    echo"<br><br><br>";
                    echo"IDs and names of the profiles the user is following:<br><br>";
                    echo "<table>";
                    for ($i=0;$i<count($friends_ids);$i++){
                        echo "<tr><td>".$friends_ids[$i]."</td><td>".$friends_names[$i]."</td></tr>";
                    }
                    echo "</table>";
                    /*echo "<br><br>names of the profiles the user is following:<br><br>";
                    for ($i=0;$i<count($friends_names);$i++){
                        echo "- ".$friends_names[$i]."<br>";
                    }*/
                    echo "<br><br>Latest tweets:<br><br>";
                    for ($i=0;$i<count($tweets);$i++){
                    	echo "- ".$tweets[$i]."<br>";
                    }
                }
            }
        ?>
        
  </body>
</html>
    