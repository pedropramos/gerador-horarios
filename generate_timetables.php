<?php
ksort($_POST);

$args = "";
foreach($_POST as $x=>$x_value) {
    $args = $args . " " . urlencode($x_value);
}

$datetime = date('d/m/Y H:i:s');
$ip = $_SERVER['REMOTE_ADDR'];
$command = "/usr/bin/python horarios.py $args";

echo shell_exec("echo [$datetime] \\($ip\\) $command >> commands.log");
echo shell_exec($command);
?>
