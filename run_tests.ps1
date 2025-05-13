# Parar e remover containers existentes
docker-compose -f docker-compose.test.yml down

# Reconstruir a imagem para garantir que temos as últimas alterações
docker-compose -f docker-compose.test.yml build

# Executar os testes
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Limpar após os testes
docker-compose -f docker-compose.test.yml down
