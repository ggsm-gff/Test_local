# Docker Course Resources

![nota_1](img/Captura%20de%20pantalla%202026-08-28%20120757.png)

![nota_2](img/Captura%20de%20pantalla%202026-08-28%20120907.png)

![nota_3](img/Captura%20de%20pantalla%202026-08-28%20120952.png)

![nota_4](img/Captura%20de%20pantalla%202026-08-28%20120831.png)


### Build a image from Dockerfile
You need to have a Dockerfile in your current directory.

**DockerFile:**
```bash
FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3
```



El comando COPY se usa durante la construcción de la imagen, es decir en el build.  

## Build Docker Image

```bash
docker build -t pipeline:v3 .
```

### Explanation

- `docker build`: Creates an image from a Dockerfile.
- `-t`: Assigns a name and tag to the image.
- `pipeline`: Image name.
- `v3`: Image version tag.
- `.`: Current directory used as the build context.

### Result

Creates a Docker image named `pipeline:v3` that can later be executed with:

```bash
docker run pipeline:v3
```

![nota_5](img/Captura%20de%20pantalla%202026-08-28%20122425.png)

```bash
# The following command will append the RUN instructions to the end of the Dockerfile.
echo -e "RUN curl https://assets.datacamp.com/production/repositories/6082/datasets/31a5052c6a5424cbb8d939a7a6eff9311957e7d0/pipeline_final.zip -o /pipeline_final.zip\nRUN unzip /pipeline_final.zip\nRUN rm /pipeline_final.zip" >> Dockerfile
# Alternatively:
# 1. Open the Dockerfile using `nano Dockerfile`.
# 2. Add `RUN curl https://assets.datacamp.com/production/repositories/6082/datasets/31a5052c6a5424cbb8d939a7a6eff9311957e7d0/pipeline_final.zip -o /pipeline_final.zip` to the end of the Dockerfile.
# 3. Add `RUN unzip /pipeline_final.zip` to the end of the Dockerfile.
# 4. Add `RUN rm /pipeline_final.zip` to the end of the Dockerfile.
# 5. Save the file and exit nano using CTRL+s and CTRL+x
```

### CMD
Podemos agregar un comando de inicio mediante una instrucción en el Dockerfile. Esta instrucción es CMD. CMD acepta un único parámetro: el comando de shell que se ejecutará cuando arranque la imagen. 
El comando de shell se ejecuta cuando alguien inicia un contenedor; no se ejecuta al usar docker build para crear una imagen a partir del Dockerfile. 
Añadir una instrucción CMD a un Dockerfile no aumenta el tamaño de la imagen ni añade tiempo a la construcción. Si existen múltiples instrucciones CMD en un único Dockerfile, solo la última tendrá efecto.

![nota_6](img/Captura%20de%20pantalla%202026-08-28%20161611.png)

**Workdir** cambia el directorio de trabajo dentro de la imagen.
**User** cambia el usuario con el que se ejecutan las instrucciones dentro de la imagen, por default en ubuntu es root.
![nota_7](img/Captura%20de%20pantalla%202026-08-31%20161210.png)

### ARG 
con la instrucción ARG se crean variables con alcance limitado al Dockerfile

![nota_8](img/Captura%20de%20pantalla%202026-08-31%20162504.png)


```bash 
docker build --build-arg project_folder=/home/repl/pipeline
```
Lo anterior funciona solo para la compilación actual

### ENV
crear una variable similar al comando ARG, pero el alcance de esta no se limita a la compilación, estas variables siguen siendo accesible dentro de la imagen.
```bash
ENV DB_USER=pipeline_user
```
estas variables no se sobreescriben en tiempo de compilación.
Pero si se pueden sobrescribir en tiempo de ejecución
```bash
Docker run --env DB_USER=dummy_user my_image
```

![nota_9](img/Captura%20de%20pantalla%202026-08-31%20163907.png)

### Bind Mount
Bind mount es enlazar un directorio o fichero del host con el contenedor 

Esto se logra con el flag **"-v"** [host] : [destino]

```bash
docker run -v ~/workspace/custom.json:/worspace/custom.json ubuntu
```

### Volumes
Volumes son una opción para almacenar data en Docker, independientemente del contenedor o del host.

```bash
Docker volume create [volume_name]
Docker volume ls
Docker volume inspect # Provee metadata acerca del volumen, incluye nombre punto de entrada, opciones
Docker volume rm [volume_name]

Docker volume create sqldata
Docker volume inspect sqldata

Docker run -v sqldata:/data postgres

```


## Networking

Se puede habilitar un puerto del contenedor en el host, cada contenedor tiene su propia IP, si se mapea correctamente en al ejecutar el contenedor, no hace falta conocer esa IP del contenedor, basta con acceder a la IP del host y especificar el puerto mapeado en el contenedor. 
Por ejemplo, un host ejecuta 3 contenedores, cada contenedor tiene una app en el puerto 80.
Se puede configurar el mapeo para que usen los puertos 5001, 5002 y 5003 del host.

```bash
docker run -p [port_host]:[port_container]
Docker run -p 5501:80

docker run -d -p 61000:80 nginx:1.27-alpine
```

### EXPOSE
Se usa para mapear un puerto del host con el contenedor, esta instruccion se utiliza unicamente dentro de Dockerfile

```bash
FROM python:3.11-slim
ENTRYPOINT ["python","-mhttp.server"]
EXPOSE 8000
----------------------------

docker run pyserver
docker ps -a
#Se muestra el port pero no es accesible desde el host

docker run -P pyserver
docker ps -a
#ahora el port si es accesible desde el host, usando un puerto efimero y sin privilegios
docker inspect [container_id]
#Se muestra toda la metadata del contenedor
```

## Networks
Tipos de redes de Docker 
- bridge: permite conexiones salientes, entrantes si expuesto
- host: permite conexion entre el host y contenedores
- none: contenedor isolado de redes

```bash
docker network [command]
docker network ls
docker network create
docker network rm

docker network create my_network

docker run --network my_network ubuntu bash

docker network connect my_network ubuntu-B

docker network inspect my_network

docker run -it --network test_network alpine:3.19.2 ping -c 3 alpine_prime
```