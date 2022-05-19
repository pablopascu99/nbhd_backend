<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Localizaciones;
use App\Models\Inmuebles;
use App\Models\LugaresInteres;
use App\Models\Comentarios;

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
        $local = Localizaciones::where('municipio', '=', $localidad)->first();
        $id_localidad = $local->id;

        $in = Inmuebles::where('localizaciones_id', '=', $id_localidad)->first();
        if ($in === null) {
            $c = '"..\resources\py\scraper_yaencontre.py" '.$localidad." ".$tipo;
            $result = exec('python '.$c);
            $json_clean = str_replace("'","\"",$result);
            $json = json_decode($json_clean);
            foreach ($json as $item) {
                $inmueble = new Inmuebles;
                $inmueble->nombre = $item->nombre;
                $inmueble->precio = $item->precio;
                $inmueble->localizaciones_id = $id_localidad;
                $inmueble->imagenes = $item->imagenes;
                $inmueble->descripcion = $item->descripcion;
                $inmueble->enlace = $item->enlace;
                $inmueble->habitaciones = $item->habitaciones;
                $inmueble->banos = $item->banos;
                $inmueble->m2 = $item->metros2;
                $inmueble->tipo = $item->tipo;
                $inmueble->telefono = $item->telefono;
                $inmueble->latitud = $item->ubicacion[0];
                $inmueble->longitud = $item->ubicacion[1];
                $inmueble->caracteristicas = $item->caracteristicas;
                $inmueble->save();
            }
        }
        $in2 = Inmuebles::where('localizaciones_id', '=', $id_localidad)->get();
        return $in2;
    }

    public function getInmueble($inmuebleId)
    {   
        $inmueble = Inmuebles::where('id', '=', $inmuebleId)->first();
        return $inmueble;
    }

    public function showLugarInteres($latitud,$longitud)
    {   

        $interes = LugaresInteres::where('latitudRadius', '=', $latitud)->first();
        if ($interes === null) {
            $c = '"..\resources\py\google.py" '.$latitud." ".$longitud;
            $result = exec('python '.$c);
            $json_clean = str_replace("'","\"",$result);
            $json = json_decode($json_clean);
            foreach ($json as $item) {
                $i = new LugaresInteres;
                $i->nombre = $item->nombre;
                $i->direccion = $item->direccion;
                $i->latitud = $item->latitud;
                $i->longitud = $item->longitud;
                $i->latitudRadius = $latitud;
                $i->longitudRadius = $longitud;
                $i->telefono = $item->telefono;
                $i->puntuacion_media = $item->puntuacion_media;
                $i->media_analisis = $item->media_analisis;
                $i->save();
                $json2 = $item->reviews;
                foreach ($json2 as $item2) {
                    $c = new Comentarios;
                    $c->autor = $item2->autor;
                    $c->texto = $item2->texto;
                    $c->interes_id = $i->id;
                    $c->puntuacion = $item2->rating;
                    $c->save();
                }
            }
        }
        $interes2 = LugaresInteres::where('latitudRadius', '=', $latitud)->get();
        return $interes2;
    }

}
