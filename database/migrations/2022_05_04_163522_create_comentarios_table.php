<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateComentariosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('comentarios', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            $table->unsignedInteger('interes_id');
            $table->foreign('interes_id')->references('id')->on('lugares_interes')->onDelete('cascade')->onUpdate('cascade');
            $table->string('autor'); 
            $table->string('texto'); 
            $table->date('fecha'); 
            $table->float('puntuacion'); 
            $table->float('latitud'); 
            $table->float('longitud');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('comentarios');
    }
}
