<?php
require_once "db.php";

$imageName= $_POST['imageName'];
$imageNameArray = explode('_', $imageName);
$person = join('_', array_slice($imageNameArray, 0, count($imageNameArray)-1));


$imageIdsArray = $_POST['imageIds'];

$count = 1;
foreach ($imageIdsArray as $id) {

    $sql = $conn->prepare("UPDATE all_images SET image_order=? WHERE id=?");
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
// $response = $imageName;
// $response = $imageIdsArray[0];
echo $response;
exit;
?>