<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateLugarConsultadosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('lugar__consultados', function (Blueprint $table) {
            $table->primary('id');
            $table->timestamps();
            $table->foreignId('id_historico')->constrained('historico__usuarios');
            $table->foreignId('id_interes')->constrained('lugares__interes');
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
        Schema::dropIfExists('lugar__consultados');
    }
}
