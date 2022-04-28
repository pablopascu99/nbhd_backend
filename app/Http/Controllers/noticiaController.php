<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class noticiaController extends Controller
{
    public function localidad($localidad)
    {   
        $c = '"..\script.py" '.$localidad;
        $result = exec('python '.$c);
        $result1 = exec('ls');
        $json_clean = str_replace("'","\"",$result);
        $json = json_decode($json_clean);
        return $json_clean;
    }
}
