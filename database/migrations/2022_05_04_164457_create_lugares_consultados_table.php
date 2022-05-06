<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateLugaresConsultadosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('lugares_consultados', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            $table->unsignedInteger('historico_usuario_id');
            $table->foreign('historico_usuario_id')->references('id')->on('historico_usuarios')->onDelete('cascade')->onUpdate('cascade');
            $table->unsignedInteger('interes_id');
            $table->foreign('interes_id')->references('id')->on('lugares_interes')->onDelete('cascade')->onUpdate('cascade');
            $table->integer('num_consultas');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('lugares_consultados');
    }
}
