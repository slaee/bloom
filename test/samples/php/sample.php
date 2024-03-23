<?php

$a = 'Simple string';
function query($a) {
    echo $a;
}
query($a);

$b = $_GET['q'];
$sql = `SELECT * FROM table WHERE id = ${b}`;

if($_SERVER['REQUEST_METHOD'] === 'POST') {
    $c = $_POST['c'];
    $sql = `SELECT * FROM table WHERE id = ${c}`;
}

function SQLQuery($sql) {
    echo $sql;
}

error_reporting(0);
function Check_Admin($input)
{
    $input = iconv ('UTF-8', 'US-ASCII//TRANSLIT', $input);// "Just to Normalize the string to UTF-8
    if(preg_match("/admin/i",$input))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function send_to_api($data)
{
    print_r($data);
    $api_url = 'http://127.0.0.1:5000/login';
    $options = [
        'http' => [
            'method' => 'POST',
            'header' => 'Content-Type: application/x-www-form-urlencoded',
            'content' => $data,
        ],
    ];
    $context = stream_context_create($options);
    $result = file_get_contents($api_url, false, $context);
    
    if ($result !== false) 
    {
        echo "Response from Flask app: $result";
    } 
    else 
    {
        echo "Failed to communicate with Flask app.";
    }
}

if(isset($_POST['login-submit']))
{
	if(!empty($_POST['username'])&&!empty($_POST['password']))
	{
        $username=$_POST['username'];
		$password=md5($_POST['password']);
        if(Check_Admin($username) && $_SERVER['REMOTE_ADDR']!=="127.0.0.1")
        {
            die("Admin Login allowed from localhost only : )");
        }
        else
        {
            send_to_api(file_get_contents("php://input")); # Sending the data to the API
        }   

	}
	else
	{
		echo "<script>alert('Please Fill All Fields')</script>";
	}
}

echo "Test" .
       "Test"
        . "Test"
        ;

?>
