<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Localizaciones;
use App\Models\Inmuebles;
use App\Models\LugaresInteres;
use App\Models\Comentarios;
use App\Models\User;
use App\Models\Reviews;

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
        }
        // delete $l si el updated_at se creo hace 30 dias
        if (strtotime($l->updated_at) < strtotime('-30 days')) {
            $l->delete();
            $l1 = Localizaciones::where('municipio', '=', $localidad)->first();
            if ($l1 === null) {
                $c = '"..\resources\py\clasificador.py" '.$localidad;
                $result = exec('python '.$c);
                $json_clean = str_replace("'","\"",$result);
                $json = json_decode($json_clean);
                $local = new Localizaciones;
                $local->odio = $json->media_odio;
                $local->municipio = $localidad;
                $local->vecesConsultado = 1;
                $local->save();
            }
        } 
        else {
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

        $in = Inmuebles::where('localizaciones_id', '=', $id_localidad)->where('tipo', '=', $tipo)->first();
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
        $inmu = Inmuebles::where('localizaciones_id', '=', $id_localidad)->where('tipo', '=', $tipo)->get();
        for ($i=0; $i < count($inmu); $i++) { 
            if (strtotime($inmu[$i]->updated_at) < strtotime('-30 days')) {
                $nombre = $inmu[$i]->nombre;
                $inmu[$i]->delete();
                $c = '"..\resources\py\scraper_yaencontre.py" '.$localidad." ".$tipo;
                $result = exec('python '.$c);
                $json_clean = str_replace("'","\"",$result);
                $json = json_decode($json_clean);
                foreach ($json as $item) {
                    if ($item->nombre == $nombre) {
                        $inmu[$i] = new Inmuebles;
                        $inmu[$i]->nombre = $item->nombre;
                        $inmu[$i]->precio = $item->precio;
                        $inmu[$i]->localizaciones_id = $id_localidad;
                        $inmu[$i]->imagenes = $item->imagenes;
                        $inmu[$i]->descripcion = $item->descripcion;
                        $inmu[$i]->enlace = $item->enlace;
                        $inmu[$i]->habitaciones = $item->habitaciones;
                        $inmu[$i]->banos = $item->banos;
                        $inmu[$i]->m2 = $item->metros2;
                        $inmu[$i]->tipo = $item->tipo;
                        $inmu[$i]->telefono = $item->telefono;
                        $inmu[$i]->latitud = $item->ubicacion[0];
                        $inmu[$i]->longitud = $item->ubicacion[1];
                        $inmu[$i]->caracteristicas = $item->caracteristicas;
                        $inmu[$i]->save();
                    }
                }
            }
        }
        $in2 = Inmuebles::where('localizaciones_id', '=', $id_localidad)->where('tipo', '=', $tipo)->get();
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
        } else {
            $lugares_interes = LugaresInteres::where('latitudRadius', '=', $latitud)->get();
            for ($i=0; $i < count($lugares_interes); $i++) { 
                if (strtotime($lugares_interes[$i]->updated_at) < strtotime('-30 days')) {
                    $nombre = $lugares_interes[$i]->nombre;
                    $lugares_interes[$i]->delete();
                    $c = '"..\resources\py\google.py" '.$latitud." ".$longitud;
                    $result = exec('python '.$c);
                    $json_clean = str_replace("'","\"",$result);
                    $json = json_decode($json_clean);
                    foreach ($json as $item) {
                        if ($nombre == $item->nombre) {
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
                }
            }
        }
        $interes2 = LugaresInteres::where('latitudRadius', '=', $latitud)->get();
        return $interes2;
    }

    public function getLugarInteres($lugarInteresId)
    {   
        $lugarInteres = LugaresInteres::where('id', '=', $lugarInteresId)->first();
        return $lugarInteres;
    }

    public function showReviews($lugarInteresId)
    {   
        $lugarInteres = LugaresInteres::where('id', '=', $lugarInteresId)->first();
        if ($lugarInteres === null) {
            return "No existe el lugar de interes";
        } else {
            $reviews = Comentarios::where('interes_id', '=', $lugarInteresId)->get();
            return $reviews;
        }
    }

    public function municipo_max_odio(){
        $maxOdio = localizaciones::orderBy('odio', 'desc')->first();
        return json_encode($maxOdio);
    }

    public function get_top_municipios($num){
        $municipios = Localizaciones::orderBy('vecesConsultado', 'desc')->take($num)->get();
        return json_encode($municipios);
    }

    public function updateUser(Request $request, $id) {
        $user = User::where('id', '=', $id)->first();
        if ($user === null) {
            return "No existe el usuario";
        } else {
            $user->email = $request->input('email');
            $user->password = bcrypt($request->input('password'));
            $user->save();
            return 200;
        }
    }

    public function get_id_localidad($localidad){
        $id = Localizaciones::select('id')->where('municipio', "=", $localidad)->first();
        return $id;
    }

    public function get_num_inmuebles($num){
        $municipos_id = array();
        $respuesta = array();
        $top_municipios = $this->get_top_municipios($num);
        for($i = 0; $i < count($top_municipios); $i++){
            $id = $this->get_id_localidad($top_municipios[$i]['municipio']);
            array_push($municipos_id, $id);
        }
        for($i = 0; $i < count($municipos_id); $i++){
            $num_inmuebles = Inmuebles::where("localizaciones_id", "=", $municipos_id[$i]['id'])->count();
            $dato = array($top_municipios[$i]['municipio'] => $num_inmuebles);
            array_push($respuesta, $dato);
        }
        return $respuesta;
    }

}
