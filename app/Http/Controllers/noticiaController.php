<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class noticiaController extends Controller
{
    public function showOdio($localidad)
    {   
        $c = '"..\resources\py\clasificador.py" '.$localidad;
        $result = exec('python '.$c);
        $json_clean = str_replace("'","\"",$result);
        $json = json_decode($json_clean);
        return $json;
    }

    public function showInmuebles($localidad,$tipo)
    {   
        $c = '"..\resources\py\scraper_yaencontre.py" '.$localidad." ".$tipo;
        $result = exec('python '.$c);
        $json_clean = str_replace("'","\"",$result);
        $json = json_decode($json_clean);
        return $json;
    }

}
