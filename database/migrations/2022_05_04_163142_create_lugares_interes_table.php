<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateLugaresInteresTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('lugares_interes', function (Blueprint $table) {
            $table->increments('id'); 
            $table->timestamps();
            $table->unsignedInteger('localizaciones_id');
            $table->foreign('localizaciones_id')->references('id')->on('localizaciones')->onDelete('cascade')->onUpdate('cascade');
            $table->string('nombre');
            $table->string('direccion');
            $table->float('latitud');
            $table->float('longitud');
            $table->json('tipo_establecimiento'); 
            $table->string('telefono');
            $table->float('puntuacion_media');  
            $table->float('media_analisis');
            $table->json('reviews');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('lugares_interes');
    }
}
