<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Scraper</title>
<?php 
	$servername       = 'localhost';
	$username         = 'root';
	$password         = '';
	$db_name          = 'pokemon_test1';
	
	$submitPressed    = isset( $_POST[ 'submit1' ] );
	$validReturnValue = 0;

	//create connection
	$conn             = new mysqli($servername, $username, $password, $db_name);


	//check successful connection
	if ($conn->connect_error) {
    	die("Connection failed: " . $conn->connect_error);
	}
	//to delete null rows
	// $sql              = "SELECT * FROM list WHERE name='NULL'";
	// $done             = mysqli_query( $conn, $sql );
	//query database and get desired pokemon
	if ( $submitPressed ) {
		$submitValue = $_POST[ 'submitValue' ];
		if ($validReturnValue = getPokemonDetails( $submitValue, $conn )) {
			$onePokemonStats = $validReturnValue;
		}
	} 
?>
</head>
<body>
<?php

//function to get pokemon from db
function getPokemonDetails( $var, $conn ) {

	/*if (preg_match('/[\'^£$%&*()}{@#~?><>,|=_+¬-]/', $var)) {
    	echo 'You think you elite hax0r? n00b.';
    	return 0;
	}*/

	$sql = "SELECT * FROM list WHERE name='".$var."'";
	if( $result = mysqli_query( $conn, $sql ) ) {
	    if(mysqli_num_rows( $result ) > 0) {
	    	$row = mysqli_fetch_array( $result );
	    	return $row;		
		} else {
			echo 'No results were found';
			return 0;
		}
	} else {
		echo 'Could\'nt make SQL connection. ';
		echo mysqli_error($conn);
		return 0;
	}
}
$sql = "SELECT * FROM list WHERE name='NULL'";
mysqli_query( $conn, $sql )
//store return values

if ( $validReturnValue ) {
	$id        = $onePokemonStats[ 0 ];
	$name      = $onePokemonStats[ 1 ];
	$type      = $onePokemonStats[ 2 ];
	$abilities = $onePokemonStats[ 3 ];
	$hp        = $onePokemonStats[ 4 ];
	$attack    = $onePokemonStats[ 5 ];
	$defense   = $onePokemonStats[ 6 ];
	$sp_atk    = $onePokemonStats[ 7 ];
	$sp_def    = $onePokemonStats[ 8 ];
	$speed     = $onePokemonStats[ 9 ];
	$bst       = $onePokemonStats[ 10 ];
	$weight    = $onePokemonStats[ 11 ];
	$height    = $onePokemonStats[ 12 ];
} else {
	$id   ='';
	$name ='';
	$type ='';
	$abilities ='';
	$hp ='';
	$attack ='';
	$defense ='';
	$sp_atk ='';
	$sp_def ='';
	$speed ='';
	$bst = '';
	$weight = '';
	$height = '';
}





?>
</div>

<!--form to get user input-->
<form name="form1" action="Scraper.php" method="POST">
    Enter Pokemon to search:
    <input type="text" name="submitValue" id="val1" value=""></input>

    <br></br>

    <input type="submit" name="submit1" value="search"></input>
</form>
<div>
<?php
//write values here of result
echo 'ID: '.$id.'<br>';
echo 'Name: '.$name.'<br>';
echo 'Type: '.$type.'<br>';
echo 'Abilities: '.$abilities.'<br>';
echo 'HP: '.$hp.'<br>';
echo 'Attack: '.$attack.'<br>';
echo 'Defense: '.$defense.'<br>';
echo 'Sp. Atk: '.$sp_atk.'<br>';
echo 'Sp. Def: '.$sp_def.'<br>';
echo 'Speed: '.$speed.'<br>';
echo 'Base Stat Total: '.$bst.'<br>';
echo 'Weight: '.$weight.' kg<br>';
echo 'Height: '.$height.' m<br>';

?>
</body>
</html>


      
