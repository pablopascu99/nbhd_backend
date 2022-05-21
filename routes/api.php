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

Route::get('/localidad/{localidad}', [noticiaController::class,'showOdio']);

Route::get('/inmuebles/{localidad}/{tipo}', [noticiaController::class,'showInmuebles']);

Route::get('/inmuebles/{inmuebleId}', [noticiaController::class,'getInmueble']);

Route::get('/lugar_interes/{latitud}/{longitud}', [noticiaController::class,'showLugarInteres']);

Route::group([
    'middleware' => 'api',
    'prefix' => 'v1/auth'

], function ($router) {
    Route::post('login', [\App\Http\Controllers\AuthController::class, 'login'])->name('login');
    Route::post('logout', [\App\Http\Controllers\AuthController::class, 'logout'])->name('logout');
    Route::post('refresh', [\App\Http\Controllers\AuthController::class, 'refresh'])->name('refresh');
    Route::post('me', [\App\Http\Controllers\AuthController::class, 'me'])->name('me');
});