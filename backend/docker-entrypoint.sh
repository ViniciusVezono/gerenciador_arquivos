set -e

echo "Aguardando banco de dados ficar disponível..."
timeout=30
counter=0
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_SERVER" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
    counter=$((counter + 1))
    if [ $counter -gt $timeout ]; then
        echo "Erro: banco de dados não ficou disponível a tempo"
        exit 1
    fi
    echo "Aguardando... ($counter/$timeout)"
    sleep 1
done

echo "Banco de dados disponível!"

echo "Executando migrations..."
python -m alembic upgrade head

echo "Iniciando servidor..."
exec "$@"