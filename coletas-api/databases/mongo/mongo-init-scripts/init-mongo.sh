#!/bin/bash

sleep 10

MONGO_URI="mongodb://localhost:27017"
DB_NAME="coletas_db"

mongo --host localhost --port 27017 <<EOF
use $DB_NAME;

db.createCollection('processos_primeira_instancia_tjal');
db.createCollection('processos_primeira_instancia_tjce');
db.createCollection('processos_segunda_instancia_tjal');
db.createCollection('processos_segunda_instancia_tjce');

db.processos_primeira_instancia_tjal.createIndex({ numero_do_processo: 1 });
db.processos_primeira_instancia_tjce.createIndex({ numero_do_processo: 1 });
db.processos_segunda_instancia_tjal.createIndex({ numero_do_processo: 1 });
db.processos_segunda_instancia_tjce.createIndex({ numero_do_processo: 1 });

EOF