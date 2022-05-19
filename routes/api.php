<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\NoticiaController;

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

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('/localidad/{localidad}', [noticiaController::class,'showOdio']);

Route::get('/inmuebles/{localidad}/{tipo}', [noticiaController::class,'showInmuebles']);

Route::get('/inmuebles/{inmuebleId}', [noticiaController::class,'getInmueble']);

Route::get('/lugar_interes/{latitud}/{longitud}', [noticiaController::class,'showLugarInteres']);