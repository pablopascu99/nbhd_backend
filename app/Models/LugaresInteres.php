<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class LugaresInteres extends Model
{
    use HasFactory;

    protected $casts = [
        'tipo_establecimiento' => 'array',
        'reviews' => 'array'
    ];
}
