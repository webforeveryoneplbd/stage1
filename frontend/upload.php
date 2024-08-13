<?php
$target_dir = "uploads/";
$files = array("file1", "file2", "file3");

foreach ($files as $file) {
    $target_file = $target_dir . basename($_FILES[$file]["name"]);
    if (move_uploaded_file($_FILES[$file]["tmp_name"], $target_file)) {
        echo "The file ". basename($_FILES[$file]["name"]). " has been uploaded.\n";
    } else {
        echo "Sorry, there was an error uploading your file: " . $_FILES[$file]["name"] . "\n";
    }
}
?>
