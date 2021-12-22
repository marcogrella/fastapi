# imagem seguida da versão

FROM python:3.9.9       

 # opcional, onde roda os comandos.
WORKDIR /user/src/app

 # copia o arquivo para o repositório no qual ficará a imagem.
COPY requirements.txt /user/src/app 

 # roda o arquivo requirements.
RUN pip install --no-cache-dir -r requirements.txt 

 # Copia tudo do diretório atual para o que está na definido no WorkDir
COPY . .

 # Comando para levantar a aplicaação.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]

