<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Localizaciones;

class noticiaController extends Controller
{
    public function showOdio($localidad)
    {   
        $l = Localizaciones::where('municipio', '=', $localidad)->first();
        if ($l === null) {
            $c = '"..\resources\py\clasificador.py" '.$localidad;
            $result = exec('python '.$c);
            $json_clean = str_replace("'","\"",$result);
            $json = json_decode($json_clean);
            $local = new Localizaciones;
            $local->odio = $json->media_odio;
            $local->municipio = $localidad;
            $local->vecesConsultado = 1;
            $local->save();
        } else {
            $local = Localizaciones::where('municipio', '=', $localidad)->first();
            $local->increment('vecesConsultado');
        }
        $l2 = Localizaciones::where('municipio', '=', $localidad)->first();
        return json_encode($l2);
    }

    public function showInmuebles($localidad,$tipo)
    {   
        $c = '"..\resources\py\scraper_yaencontre.py" '.$localidad." ".$tipo;
        $result = exec('python '.$c);
        $json_clean = str_replace("'","\"",$result);
        $json = json_decode($json_clean);
        // $lista_nombres = array();
    
        // for ($i = 0; $i <= (count($json)-1); $i++) {
        //     $data=array('nombre'=>$json[$i]->nombre,"m2"=>$json[$i]->metros2,"precio"=>$json[$i]->precio,"banos"=>$json[$i]->banos,"descripcion"=>$json[$i]->descripcion);
        //     Inmuebles::table('student_details')->insert($data);
        // }
        return $json;
    }

}
