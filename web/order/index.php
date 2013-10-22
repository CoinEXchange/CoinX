<!DOCTYPE HTML PUBLIC 
   "-//W3C//DTD HTML 4.0 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd" > 
<!-- Beginn HTML-Kopf -->
<html>
<head>
  <title>Order</title>
<script>
function myPwd() {

        var x;

        var pwd = prompt("Please enter your receiving address", "Write Here Something");

        if (pwd != null) {

            x = "Welocme at " + site + "! Have a good day";

            document.getElementById("demo").innerHTML = x;

        }

    }
</script>
<style type="text/css">
body {
background-color: #FFFFFF;
padding:10px 10px 10px 10px;
font-size: 12px;
font-family:Arial, Verdana, Tahoma, Helvetica, sans-serif;
color:#3F3F3F;
}

a{
color:#00007F;
text-decoration: none;
}

a:hover{
color:#FF5F00;
text-decoration: none;
}

a:active{
color:#00007F;
text-decoration: none;
}

.input {
padding-left:5px;
padding-right:5px;
-moz-border-radius:4px;
-webkit-border-radius:4px;
border-radius: 4px;
background-color:#FFFFFF;
border: 1px solid #CFCFCF;
height:30px;
font-size: 12px;
color:#5F5F5F;
-moz-box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
-webkit-box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.button {
background: -webkit-gradient( linear, left top, left bottom, color-stop(0.05, #0000DF), color-stop(1, #0070C0) );
background: -moz-linear-gradient( center top, #0000DF 5%, #0070C0 100% );
filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#0000DF', endColorstr='#0070C0');
background-color: #0060FF;
-moz-border-radius: 4px;
-webkit-border-radius: 4px;
border-radius: 4px;
height:30px;
border: 1px solid #0000FF;
display: inline-block;
color: #EFEFEF;
font-size: 14px;
font-weight: bold;
font-face: arial;
padding: 6px 24px;
text-decoration: none;
cursor: pointer;
}
</style>
</head>
<!-- Ende HTML-Kopf -->



<body>
<h1>Order</h1>
SCUR: <?php print $_POST['scur']; ?></p>
SELL: <?php print $_POST['sell']; ?></p>
BCUR: <?php print $_POST['bcur']; ?></p>
BUY: <?php print $_POST['buy']; ?></p>
RTADR: <?php print $_POST['rtadr']; ?></p>
RCADR: <?php print $_POST['rcadr']; ?> (hidden)</p>
<hr>
<form method="POST" action="index.php">
<?php
$verbindung = mysql_connect ("dontoc.dlinkddns.com",
			     "jack", "hammer")
  or die ("keine Verbindung möglich.
 Benutzername oder Passwort sind falsch");

mysql_select_db("btcltc_TK")
or die ("Die Datenbank existiert nicht.");
?>
<table>
Sell: <input name="sell" type="text" size="10" maxlength="10" value="<?print $_POST['sell']?>">
<select name="scur" size="1">
<?php $abfrage = "SELECT cur FROM btcltc_TK.currencies";
$ergebnis = mysql_query($abfrage)
  OR die("Error: $abfrage <br>".mysql_error());

while($row = mysql_fetch_object($ergebnis))
  {
    echo "<option";
    if ($row->cur == $_POST['scur']) {echo " selected";}
    echo ">";
    echo "$row->cur</option>";
  }
?>
</select>
</p>


Buy: <input name="buy" type="text" size="10" maxlength="10"value="<?print $_POST['buy']?>">
<select name="bcur" size="1">
<?php $abfrage = "SELECT cur FROM btcltc_TK.currencies";
$ergebnis = mysql_query($abfrage)
  OR die("Error: $abfrage <br>".mysql_error());

while($row = mysql_fetch_object($ergebnis))
  {
    echo "<option";
    if ($row->cur == $_POST['bcur']) {echo " selected";}
    echo ">";
    echo "$row->cur</option>";
  }
?>
</select>
Address to receive funds: <input name="rtadr" type="text" size="30" maxlength="30"  value="<?print $_POST['rtadr']?>">
<input type="hidden" name="rcadr" type="text">
</table>
</p>
<input type="submit" value="Generate Order">
</form>
<button onclick="myPwd()">Prompt Box</button>

<p id="demo"></p>
</body>
</html>

