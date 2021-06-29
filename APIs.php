<?php
include_once("msql-connection.php");
$curl = curl_init();

$id_list = array('tt8703836', 'tt0119217', 'tt1013648', 'tt3147520', 'tt7314598', 'tt0372784', 'tt2975590', 'tt0096895', 'tt0103776', 'tt0112462', 'tt0118688', 'tt4116284', 'tt0103359', 'tt1569923', 'tt2313197', 'tt2705436', 'tt2084949', 'tt0100669', 'tt1785572', 'tt1132238', 'tt1433184', 'tt2233044', 'tt5978586', 'tt2586634', 'tt6889550', 'tt0232500', 'tt0463985', 'tt0046969', 'tt0878117', 'tt4106374', 'tt1008725', 'tt2353948', 'tt0843849', 'tt0781022', 'tt0781023', 'tt2975590', 'tt0348150', 'tt0078346', 'tt0081573', 'tt0086393', 'tt0094074', 'tt1673430', 'tt1398941', 'tt0106057', 'tt0934706', 'tt0954542', 'tt0162408', 'tt0231426', 'tt0311343', 'tt0382268', 'tt0480409', 'tt0806096', 'tt0925222', 'tt1129377', 'tt1129378', 'tt0458339', 'tt1843866', 'tt3498820', 'tt0103923', 'tt3911200', 'tt0078937', 'tt0078938', 'tt0206474', 'tt0036697', 'tt1740721', 'tt0758758', 'tt1054487', 'tt4228738', 'tt1200063', 'tt1200064', 'tt1224033', 'tt3431736', 'tt11714514', 'tt1141651', 'tt8589192', 'tt0047478', 'tt0814314', 'tt1931533', 'tt2404435', 'tt0029583', 'tt0120102', 'tt0054047', 'tt0120828', 'tt0165982', 'tt0048605', 'tt3322940', 'tt5140878', 'tt8350360', 'tt0323120', 'tt0154152', 'tt0229217', 'tt3032060', 'tt0203883', 'tt0241185', 'tt2361433', 'tt1457767', 'tt3065204', 'tt7069210', 'tt2425866', 'tt6951902', 'tt7904362', 'tt9233860', 'tt0384008', 'tt11540274', 'tt0996924');


foreach($id_list as $id)
{
    curl_setopt_array($curl, [
	CURLOPT_URL => "https://movie-database-imdb-alternative.p.rapidapi.com/?i=".$id."&page=1&r=json",
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_FOLLOWLOCATION => true,
	CURLOPT_ENCODING => "",
	CURLOPT_MAXREDIRS => 10,
	CURLOPT_TIMEOUT => 30000,
	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
	CURLOPT_CUSTOMREQUEST => "GET",
	CURLOPT_HTTPHEADER => [
		"x-rapidapi-host: movie-database-imdb-alternative.p.rapidapi.com",
		"x-rapidapi-key: 9a2be66f9amsh1f3aa48f360a496p197215jsn3210fc010dbe"
	],
]);

$res = curl_exec($curl);
$res = json_decode($res,true);
$err = curl_error($curl);

$name = $res['Title'];
$rating = $res['imdbRating'];
$date = date('Y-m-d');
$genre = $res['Genre'];
$picpath = $res['Poster'];
$synopsis = $res['Plot'];
$cast = $res['Actors'];
$runtime = $res['Runtime']=="N/A"?140:$res['Runtime'];
$trailer = "N/A";

$query = "insert into movies values('$name','$rating','$date','$genre','$picpath','$synopsis','$cast','$runtime','$trailer')";

mysqli_query($dbcon,$query);

}
curl_close($curl);
?>
