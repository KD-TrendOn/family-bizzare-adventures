echo "Starting"

alembic upgrade head

echo "OK"

exec "$@"