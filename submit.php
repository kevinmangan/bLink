<?php


    require("swift/lib/swift_required.php");
    require("unirest/lib/Unirest.php");
    require("sendgrid/SendGrid.php");
    SendGrid::register_autoloader();


    $sendgrid_username = 'app22130497@heroku.com';
    $sendgrid_password = 'pumet1eb';
    $sendgrid = new SendGrid($sendgrid_username, $sendgrid_password);

    $message = '<html><body>';
    $message .= '<table rules="all" style="border-color: #666;" cellpadding="10">';
    $message .= "<tr style='background: #eee;'><td><strong>First Name:</strong> </td><td>" . strip_tags($_POST['firstName']) . "</td></tr>";
    $message .= "<tr><td><strong>Last Name:</strong> </td><td>" . strip_tags($_POST['lastName']) . "</td></tr>";
    $message .= "<tr><td><strong>Email:</strong> </td><td>" . strip_tags($_POST['email']) . "</td></tr>";
    $message .= "<tr><td><strong>Phone:</strong> </td><td>" . strip_tags($_POST['school']) . "</td></tr>";
    $message .= "</table>";
    $message .= "<br><br><br></body></html>";

    $mail = new SendGrid\Email();
    $mail->addTo('soppenheim14@gsb.columbia.edu')->setFrom(strip_tags($_POST['email']))->setSubject('B-Link Submission')->setHtml($message);
    
    $sendgrid->smtp->send($mail);

?>


<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">

    <title>Business Link</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="cover.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="site-wrapper">

      <div class="site-wrapper-inner" style="vertical-align: middle;">

        <div class="cover-container">
          
          <div class="inner cover" >
            <h1 class="cover-heading">Thank you for your submission</h1>
            <p class="lead">Blah Blah Blah</p>
          </div>

        <br>

            
              
              
              

          <div class="mastfoot">
            <div class="inner">
              <p>Business Link 2014</p>
            </div>
          </div>

        </div>

      </div>

    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/docs.min.js"></script>
  </body>
</html>