<?php
require_once "db.php";
$curl = curl_init("PYTHON_URL/random"); 
$html = curl_exec($curl);
curl_close($curl);
$imageName = $_GET["imageName"];
$imageNameArray = explode('_', $imageName);

$person = join('_', array_slice($imageNameArray, 0, count($imageNameArray)-1));
$sql = "SELECT * FROM all_images where person='" . $person . "' order by image_order asc;";
$result = $conn->query($sql);
$conn->close();


?>
<!doctype html>
<html >
    <head>

        <script src="vendor/jquery/jquery-3.2.1.min.js"></script>

        <link rel="stylesheet" href="vendor/jquery/jquery-ui/jquery-ui.css">
        <script src="vendor/jquery/jquery-ui/jquery-ui.js" type="text/javascript"></script>
        
        <link rel="stylesheet" type="text/css" href="style4.css" >
       
        <title>Change Order of Images in Photo Gallery with Drag and Drop using PHP AJAX</title>
        <script>
            function getQueryVariable(variable) {
                var query = window.location.search.substring(1);
                var vars = query.split("&");
                for (var i=0;i<vars.length;i++) {
                    var pair = vars[i].split("=");
                    if (pair[0] == variable) {
                        return pair[1];
                    }
                    } 
                 alert('Query Variable ' + variable + ' not found');
            }
            var imageName = getQueryVariable('imageName');
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
//                             window.alert(split_id[1]);
                        }
                    });
                    $.ajax({
                        url: 'reorder_update_particular_person.php',
                        type: 'post',
                        data: {imageIds: imageIdsArray , imageName: imageName},
                        success: function (response) {
//                            $("#txtresponse").css('display', 'inline-block'); 
//                            $("#txtresponse").text(response);
//                            location.reload()
                              window.alert(response);
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

                        echo '<li id="image_' . $imageId . '">
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
      <h2>              </h2> 
      <p>    g </p>
      <p>Click below to show the sorted images </p> 
      <button onclick="myFunc()">Click me</button> 
      <!~~script to redirect to another webpage~~>   
      <script> 
         function myFunc() { 
          location.replace("elo.php"); 
         } 
      </script> 

    </body>
</html>