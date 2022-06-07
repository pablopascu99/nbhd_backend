<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\NoticiaController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\AuthController;


/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::get('/localidad/{localidad}', [noticiaController::class,'showOdio']);

Route::get('/inmuebles/{localidad}/{tipo}', [noticiaController::class,'showInmuebles']);

Route::get('/inmuebles/{inmuebleId}', [noticiaController::class,'getInmueble']);

Route::get('/lugar_interes/{latitud}/{longitud}', [noticiaController::class,'showLugarInteres']);

Route::get('/lugar_interes/{lugarInteresId}', [noticiaController::class,'getLugarInteres']);

Route::get('/reviews/{lugarInteresId}', [noticiaController::class,'showReviews']);

Route::get('/get_top_municipios/{num}', [noticiaController::class, 'get_top_municipios']);

Route::put('/usuarios/actualizar_email/{id}', [noticiaController::class, 'updateUserEmail']);

Route::put('/usuarios/actualizar_password/{id}', [noticiaController::class, 'updateUserPass']);

Route::get('/get_max_municipio_odio', [noticiaController::class, 'municipo_max_odio']);

Route::get('/get_num_inmuebles/{num}', [noticiaController::class, 'get_num_inmuebles']);

Route::get('/get_nombre_localidad/{id_localidad}', [noticiaController::class, 'get_nombre_localidad']);


Route::group([
    'middleware' => 'api',
    'prefix' => 'auth'
], function ($router) {
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::post('/refresh', [AuthController::class, 'refresh']);
    Route::get('/user-profile', [AuthController::class, 'userProfile']);   
});