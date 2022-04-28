<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateInmuebleConsultadosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('inmueble__consultados', function (Blueprint $table) {
            $table->primary('id');
            $table->timestamps();
            $table->foreignId('id_historico')->constrained('historico__usuarios');
            $table->foreignId('id_interes')->constrained('inmuebles');
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
        Schema::dropIfExists('inmueble__consultados');
    }
}
