<?php
//include_once("msql-connection.php");

//$id = "coolbangers1438@gmail.com";
$command = escapeshellcmd('/Applications/XAMPP/xamppfiles/htdocs/Book-My-Movie/recommendation_system.py');

echo shell_exec($command);

?>