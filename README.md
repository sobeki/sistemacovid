# Covid World API
API com informações do covid-19, dados referentes ao repositório https://github.com/CSSEGISandData/COVID-19.

## ENDPOINTS
>GET /cases

Casos de todos países do mundo

>GET /cases/\<country>
    
Casos por país
    
>GET /recovered

Recuperações de todos países do mundo
    
>GET /recovered/\<country>
    
Recuperações por país
    
>GET /deaths

Mortes de todos países do mundo
    
>GET /deaths/\<country>
    
Mortes por país

## Para desenvolvimento

-Ter python3+

-Instalar virtualenv `pip install virtualenv`

-Inicializar virtualenv dentro do folder, comando `virtualenv ./` 

-Ativar virtualenv, `cd Scripts/ && activate && cd ..`

-Instalar dependencias, `pip install -r requirements.txt`

-Para iniciar o app para desenvolvimento, `flask run`


