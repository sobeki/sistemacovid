import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="13150993",
    database="coronavirus"
)

mycursor = mydb.cursor()


def insercao_casos(nomepaises, quantidade, data):
    sql = "INSERT INTO  Casos (quantidades, data) VALUES (%s, %s)"
    val = (quantidades, data)
    mycursor.execute(sql, val)
    # mydb.commit() # aqui é para confirma na tabela

    sql = "INSERT INTO paises (nomepaises) VALUES (%s)"
    val = (nomepaises)
    mycursor.execute(sql, val)

    if curso.lastrowid:
         print('last insert id', curso.lastrowid)
    else:
          print('last insert id not foaud')


   mydb.commit()
   mydb.commit()
    

def insercao_mortes(nome,quantidade,data):

   sql = "INSERT INTO  mortes (quantidade, data) VALUES (%s, %s)"
   val = (quantidade, data)
   mycursor.execute(sql, val)
   mydb.commit()

    # sql = "INSERT INTO paises (nomepaises) VALUES (%s)"
    # val = (nomepaises)
    # mycursor.execute(sql, val)

    # if curso.lastrowid:
    # print('last insert id', curso.lastrowid)
    # else:
    #   print('last insert id not foaud')

  # mydb.commit()
  # mydb.commit()

  # def insercao_Recuperados(nome,quantidade,data):

    # sql = "INSERT INTO Recuperados (quantidade, data) VALUES (%s, %s)"
    # val = (quantidade, data)
    # mycursor.execute(sql, val)

    # sql = "INSERT INTO paises (nomepaises) VALUES (%s)"
    # val = (nomepaises)
    # mycursor.execute(sql, val)

    # if curso.lastrowid:
    # print('last insert id', curso.lastrowid)
    # else:
    #   print('last insert id not foaud')

    # mydb.commit()
    # mydb.commit()

