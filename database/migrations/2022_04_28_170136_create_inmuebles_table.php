<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateInmueblesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('inmuebles', function (Blueprint $table) {
            $table->primary('id');
            $table->timestamps();
            $table->foreignId('id_localizacion')->constrained('localizaciones');
            $table->string('nombre');
            $table->string('categoria');
            $table->string('descripcion');
            $table->float('precio');
            $table->float('longitud');
            $table->float('latitud');
            $table->json('atributos');
            $table->json('imagenes');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('inmuebles');
    }
}
