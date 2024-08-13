<?php

// Définir les informations de connexion à la base de données
$hostName = "localhost";
$dbUser = "root";
$dbPassword = "";
$dbName = "user";

// Activer le rapport d'erreurs MySQLi pour lancer des exceptions
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

try {
    // Créer une connexion à la base de données
    $conn = new mysqli($hostName, $dbUser, $dbPassword, $dbName);
    // Définir le charset de la connexion pour éviter les problèmes d'encodage
    $conn->set_charset("utf8mb4");
} catch (Exception $e) {
    // Loguer l'erreur
    error_log($e->getMessage());
    // Terminer l'exécution du script et signaler une erreur de connexion
    exit('Error connecting to database'); // Doit être géré correctement en production
}

?>