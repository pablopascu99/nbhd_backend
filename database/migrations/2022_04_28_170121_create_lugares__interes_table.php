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
        Schema::create('lugares__interes', function (Blueprint $table) {
            $table->primary('id'); 
            $table->foreignId('id_localizacion')->constrained('localizaciones');
            $table->string('tipo_establecimiento'); 
            $table->float('puntuacion_media'); 
            $table->string('telefono'); 
            $table->float('latitud'); 
            $table->float('longitud');
            $table->string('direccion'); 
            $table->float('media_analisis');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('lugares__interes');
    }
}
