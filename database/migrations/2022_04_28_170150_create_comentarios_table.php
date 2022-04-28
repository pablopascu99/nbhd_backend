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
            $table->primary('id');
            $table->timestamps();
            $table->foreignId('id_interes')->constrained('lugares__interes');
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
