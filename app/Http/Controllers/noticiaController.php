<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class noticiaController extends Controller
{
    public function localidad($localidad)
    {   
        $c = '"..\resources\py\clasificador.py" '.$localidad;
        $result = exec('python '.$c);
        $json_clean = str_replace("'","\"",$result);
        $json = json_decode($json_clean);
        return $json_clean;
    }
}
