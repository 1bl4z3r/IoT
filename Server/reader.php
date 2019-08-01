<?php
    $Temp = $_POST["data"];
//    $Humidity = $_POST["station"];
//    $Write = $Temp . ' ' . $Humidity;
    file_put_contents('data.txt', $Temp);
     echo $Temp . '#';
?>