<?php
require_once "db.php";

$imageIdsArray = $_POST['imageIds'];

$count = 1;
foreach ($imageIdsArray as $id) {

    $sql = $conn->prepare("UPDATE tbl_images SET current_sample=? WHERE id=?");
    $imageOrder = $count;
    $imageId = $id;
    $sql->bind_param("ii", $imageOrder, $imageId);
    if ($sql->execute()) {
        $response = 'Images order is updated';
    } else {
        $response = 'Problem in Changing the Image Order';
    }
    $count ++;
}

$curl = curl_init("PYTHON_URL:89/record"); 
$html = curl_exec($curl);
curl_close($curl);
// $curl = curl_init("PYTHON_URL:89/elo"); 
// $html = curl_exec($curl);
// curl_close($curl);
echo $response;
exit;
?>