<!DOCTYPE HTML PUBLIC 
   "-//W3C//DTD HTML 4.0 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd" > 
<!-- Beginn HTML-Kopf -->
<html>
<head>
  <title>Order</title>
  <link rel="stylesheet" type="text/css" href="formate.css">
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
if (!isset($_SERVER['PHP_AUTH_USER'])) {
    header('WWW-Authenticate: Basic realm="1"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Text, der gesendet wird, falls der Benutzer auf Abbrechen drückt';
    exit;
} else {
    echo "<p>Hallo {$_SERVER['PHP_AUTH_USER']}.</p>";
    echo "<p>Sie gaben {$_SERVER['PHP_AUTH_PW']} als Passwort ein.</p>";
}
$verbindung = mysql_connect ("dontoc.dlinkddns.com",
			     "jack", "hammer")
  or die ("keine Verbindung möglich.
 Benutzername oder Passwort sind falsch");

mysql_select_db("BTCLTC_TK")
or die ("Die Datenbank existiert nicht.");
?>
<table>
Sell: <input name="sell" type="text" size="10" maxlength="10" value="<?print $_POST['sell']?>">
<select name="scur" size="1">
<?php $abfrage = "SELECT cur FROM BTCLTC_TK.currencies";
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
<?php $abfrage = "SELECT cur FROM BTCLTC_TK.currencies";
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

