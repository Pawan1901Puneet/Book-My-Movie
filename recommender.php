<?php
include_once("msql-connection.php");


$id = $_SESSION["email"]; //getting the user id
$command = escapeshellcmd("rec2.py $id");
echo "Hel";

echo shell_exec($command);

?>