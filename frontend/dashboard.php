<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RECOR Frontend</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }

        #dashboard-container {
            margin-top: 20px;
        }

        iframe {
            width: 100%;
            height: 500px;
            border: none;
            margin-top: 20px;
        }

        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }

        button:hover {
            background-color: #45a049;
        }

        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <h1>RECORE Requests</h1>
    
    <h2>Upload Files</h2>
    <form id="upload-form" action="http://127.0.0.1:8000/uploadfiles/" method="post" enctype="multipart/form-data">
        <input type="file" id="file1" name="file1" required>
        <input type="file" id="file2" name="file2" required>
        <input type="file" id="file3" name="file3" required>
        <button type="submit">Upload</button>
    </form>

    <h2>Search User</h2>
    <form id="user-form">
        <input type="text" id="matricule" placeholder="Matricule" required>
        <button type="submit">Search</button>
        
    </form>
    <h2>Update Telephone</h2>
    <form id="update-form">
        <input type="text" id="matricule1" name="matricule1" placeholder="Matricule1" required>
        <input type="text" id="telephone" name="telephone" placeholder="Telephone" required>
        <button type="submit">Update Telephone</button>
    </form>

    <pre id="user-info"></pre>
    <div class="container">
    <h1>Tableau de Bord des Avances des Agents</h1>
    <button id="start-dashboard-btn">Afficher le Tableau de Bord</button>
    
    <div id="dashboard-container">
        <!-- L'iframe pour afficher le tableau de bord Dash -->
        <iframe id="dashboard-iframe" src="" style="display:none;"></iframe>
    </div>
</div>

<script>
    document.getElementById('start-dashboard-btn').onclick = function() {
        this.disabled = true;  // Désactiver le bouton après le clic

        fetch('/start-dashboard/')
            .then(response => response.json())
            .then(data => {
                if (data.url) {
                    // Afficher le tableau de bord dans l'iframe
                    const iframe = document.getElementById('dashboard-iframe');
                    iframe.src = data.url;
                    iframe.style.display = 'block';
                } else {
                    alert('Erreur lors du démarrage du tableau de bord');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur lors du démarrage du tableau de bord');
            });
    };
</script>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="app.js"></script>
    <script>
       $(document).ready(function () {
    $('#update-form').on('submit', function (e) {
        e.preventDefault();

        var formData = new FormData();
        formData.append('matricule', $('#matricule1').val());
        formData.append('telephone', $('#telephone').val());

        $.ajax({
            url: 'http://127.0.0.1:8000/update_telephone/',
            type: 'PUT',
            data: formData,
            contentType: false,  // Important pour permettre à jQuery d'envoyer le FormData correctement
            processData: false,  // Important pour ne pas traiter les données avant l'envoi
            success: function (response) {
                alert('Telephone number updated successfully');
            },
            error: function (jqXHR) {
    var errorMessage = JSON.stringify(jqXHR.responseJSON.detail, null, 2);
    alert('Error updating telephone number: ' + errorMessage);
}

        });
    });
});

    </script>
</body>
</html>
