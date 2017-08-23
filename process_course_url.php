<?php

$id = intval($_POST["course_id"]);
$url = urlencode($_POST["url"]);

$datetime = date('d/m/Y H:i:s');
$ip = $_SERVER['REMOTE_ADDR'];
$command = "/usr/bin/python process_course_url.py $id $url";

echo shell_exec("echo [$datetime] \\($ip\\) $command >> commands.log");
echo shell_exec($command);
?>
