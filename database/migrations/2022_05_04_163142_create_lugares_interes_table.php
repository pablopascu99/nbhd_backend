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
            /*$table->unsignedInteger('localizaciones_id');
            $table->foreign('localizaciones_id')->references('id')->on('localizaciones')->onDelete('cascade')->onUpdate('cascade');*/
            $table->string('nombre')->nullable();
            $table->text('direccion')->nullable();
            $table->string('latitud')->nullable();
            $table->string('longitud')->nullable();
            $table->string('longitudRadius')->nullable();
            $table->string('latitudRadius')->nullable();
            $table->json('tipo_establecimiento')->nullable(); 
            $table->string('telefono')->nullable();
            $table->string('puntuacion_media')->nullable();  
            $table->string('media_analisis')->nullable();
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
