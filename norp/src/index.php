<?php
require_once "db.php";
$sql = "SELECT * FROM tbl_images ORDER BY image_order ASC";
$result = $conn->query($sql);
$conn->close();
?>
<!doctype html>
<html >
    <head>

        <script src="vendor/jquery/jquery-3.2.1.min.js"></script>

        <link rel="stylesheet" href="vendor/jquery/jquery-ui/jquery-ui.css">
        <script src="vendor/jquery/jquery-ui/jquery-ui.js" type="text/javascript"></script>
        
        <link rel="stylesheet" type="text/css" href="style2.css" >
       
        <title>Change Order of Images in Photo Gallery with Drag and Drop using PHP AJAX</title>
        <script>
            $(document).ready(function () {
                var dropIndex;
                $("#image-list").sortable({
                    	update: function(event, ui) { 
                    		dropIndex = 1000000000;
                    }
                });

                $('#submit').click(function (e) {
                    var imageIdsArray = [];
                    $('#image-list li').each(function (index) {
                        if(index <= dropIndex) {
                            var id = $(this).attr('id');
                            var split_id = id.split("_");
                            imageIdsArray.push(split_id[1]);
                        }
                    });

                    $.ajax({
                        url: 'reorderUpdate.php',
                        type: 'post',
                        data: {imageIds: imageIdsArray},
                        success: function (response) {
                           $("#txtresponse").css('display', 'inline-block'); 
                           $("#txtresponse").text(response);
                        }
                    });
                    e.preventDefault();
                });
            });

        </script>
    </head>
    <body>
        <div id="gallery">
        
        <div id="image-container">
        <h2>Change Order of Images with Drag and Drop</h2>
        <div id="txtresponse" > </div>
            <ul id="image-list" >
                <?php
                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {

                        $imageId = $row['id'];
                        $imageName = $row['image_name'];
                        $imagePath = $row['image_path'];

                        echo '<li id="image_' . $imageId . '" >
                        <img src="' . $imagePath . '" alt="' . $imageName . '"></li>';
                    }
                }
                ?>
            </ul>

        </div>            
        <div id="submit-container"> 
            <input type='button' class="btn-submit" value='Submit' id='submit' />
        </div>
        </div>
    </body>
</html>