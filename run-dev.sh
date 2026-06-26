#!/bin/bash
set -e

echo "Iniciando configuração do ambiente de desenvolvimento..."

if [ ! -f "./backend/.env" ]; then
    echo "Criando .env do backend a partir do exemplo..."
    cp ./backend/.env.example ./backend/.env
else
    echo "Arquivo .env do backend já existe."
fi

if [ ! -f "./frontend/.env.local" ]; then
    echo "Criando .env.local do frontend a partir do exemplo..."
    cp ./frontend/.env.example ./frontend/.env.local
else
    echo "Arquivo .env.local do frontend já existe."
fi

echo "Construindo e subindo os containers com Docker Compose..."
docker compose up -d --build

echo "Ambiente configurado e rodando com sucesso!"