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
        Schema::create('users', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            // $table->unsignedInteger('historico_usuario_id');
            // $table->foreign('historico_usuario_id')->references('id')->on('historico_usuarios')->onDelete('cascade')->onUpdate('cascade');
            $table->string('name');
            $table->string('email_verified_at');
            $table->string('email');
            $table->string('password');
            $table->string('remember_token');
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
