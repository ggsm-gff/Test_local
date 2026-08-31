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