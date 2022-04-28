<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateUsuariosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('usuarios', function (Blueprint $table) {
            $table->primary('id');
            $table->timestamps();
            $table->foreignId('id_historico')->constrained('historico__usuarios');
            $table->string('nombre');
            $table->string('apellidos');
            $table->string('email');
            $table->string('password');
            $table->integer('usuario_rol');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('usuarios');
    }
}
