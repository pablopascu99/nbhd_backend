<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use GuzzleHttp\Client;

class homeController extends Controller
{
    public function hola()
    {   

        $result = exec('python "C:\Users\pablo 2\ejemplo\script.py"');
        $json_clean = str_replace("'","\"",$result);
        $json = var_dump(json_decode($json_clean));
        // echo ($result);
        return $json_clean;
    }

    public function localidad($localidad)
    {   
        return $localidad;
    }

}