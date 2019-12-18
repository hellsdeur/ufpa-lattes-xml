import pandas as pd
import xml.dom.minidom as mnd
import zipfile
import os
import shutil

def descompactar(path):
    arquivos = os.listdir(path) #lista zips da pasta
    
    for file in arquivos: # unzip cada arquivo em pastas deiferentes
        dirname = file[0:-4]
        os.mkdir(path + '/' + dirname)
        zipado = zipfile.ZipFile(path + '/' + file)
        os.chdir(path + '/' + dirname)
        zipado.extractall()
        os.chdir(path)
        zipado.close()
    
    for file in arquivos: # remove arquivos zip
        os.remove(path + '/' + file)

def extrair_nomesCompletos(path, roo_t, child1, *argv):
    doc = mnd.parse(path);
    contador = -1

    root = doc.getElementsByTagName(roo_t);  # Pega o root dos currículos

    child_dadosGerais = [];  # Cria uma lista para o endereço da child que serão inseridas aqui

    atributos = []  # Cria uma lista para armazenar o atributo da child
    atributos_Tag = []  # Lista para armazenar a Tag dos atributos

    dic = {}  # Dicionário que será retornado no final da função

    for i in root:
        child_dadosGerais.append(
            i.getElementsByTagName(child1))  # Adiciona o endereço da respectiva child nas listas child_X

    for arg in argv:
        contador += 1  # Contador para alocar os atributos em seus devidos lugares
        atributos.append([])  # Cria uma sub-lista que irá armazenar os atributos de cada Tag separadamente
        atributos_Tag.append(arg)  # Adiciona a Tag em questão na lista de Tag

        for i in child_dadosGerais:
            atributos[contador].append(i[0].attributes[
                                           arg].value)  # Tenta buscar o atributo na primeira child, se não for encontrado parte para o segundo

    for i in range(len(atributos)):
        dic[atributos_Tag[i]] = (
        atributos[i])  # Adiciona para cada chave a tupla contendo todos elementos da sublista em questão

    contador = 0
    for j in range(len(atributos[0])):  # Serve para a próxima função, uma vez que precisamos fazer uma iteração de todas linhas presentes no excel
        contador += 1

    return atributos

def get_Caminhos(path): # pegar caminhos dos arquivos
    folders = []
    filepaths = []
    
    for folder in os.listdir(path): # pegar o nome das pastas
        folders.append(folder)
    
    for folder in folders: # adicionar o resto da string
        filepath = path + '/' + folder + '/curriculo.xml'
        filepaths.append(filepath) # lista de caminhos
        
    return filepaths # lista com caminhos

def get_filenames_nomesCompletos(path):
    nomesCompletos = [] 
    filenames = []
    
    filepaths = get_Caminhos(path) # obtem caminhos

    for i in filepaths: # obtem nomes completos
        nome = extrair_nomesCompletos(i, "CURRICULO-VITAE", 'DADOS-GERAIS', 'NOME-COMPLETO')
        nomesCompletos.append(nome[0][0])
    
    for nome in nomesCompletos: # formata cada filename
        palavras = nome.split(' ')
        nomeCaminho = '_'.join(palavras)
        nomeCaminho += '.xml'
        filenames.append(nomeCaminho)
        
    return filenames, nomesCompletos

def renomearXmls(path,filenames):
    listaFolder = os.listdir(path)
    for i in range(len(listaFolder)):
        shutil.move(path + '/' + listaFolder[i] + '/' + 'curriculo.xml', path + '/' + 'curriculo.xml')
        filenames[i] = path + '/' + filenames[i]
        os.rename(path + '/' + 'curriculo.xml', filenames[i])
        
    for folder in listaFolder:
        os.rmdir(path + '/' + folder)

def juntar_professores(filename, nomes_completos):
    trabalhos_em_eventos = []
    artigos_publicados = []
    capitulos_publicados = []
    apresentacoes_trabalho = []
    lista_geral = []
    
    for name, comp_name in zip (filename, nomes_completos):
        a = extrair_Info(name, comp_name)
        trabalhos_em_eventos.append(a[0])
        artigos_publicados.append(a[1])
        capitulos_publicados.append(a[2])
        apresentacoes_trabalho.append(a[3])
    lista_geral.append(trabalhos_em_eventos)
    lista_geral.append(artigos_publicados)
    lista_geral.append(capitulos_publicados)
    lista_geral.append(apresentacoes_trabalho)
    
    return lista_geral

def extrair_Info(filename, nomes):
    def extrair_info(path, roo_t, child1, child2, *argv):
        doc = mnd.parse(path);
        contador = -1
        root = doc.getElementsByTagName(roo_t); #Pega o root dos currículos
        
        child_dadosBasicos = []; #Cria uma lista para o endereço de todas as child que serão inseridas aqui e na lista posterior
        child_detalhamento = [];
    
        atributos = [] #Cria uma lista para armazenar o atributo de todas child
        atributos_Tag = [] #Lista para armazenar a Tag dos atributos
        
        dic = {}#Dicionário que será retornado no final da função
    
        for i in root:
            child_dadosBasicos.append( i.getElementsByTagName(child1)) #Adiciona o endereço da respectiva child nas listas child_X
            child_detalhamento.append( i.getElementsByTagName(child2))
            
        for arg in argv:
            contador += 1 #Contador para alocar os atributos em seus devidos lugares
            atributos.append([]) #Cria uma sub-lista que irá armazenar os atributos de cada Tag separadamente
            atributos_Tag.append(arg) #Adiciona a Tag em questão na lista de Tag
            for i, j in zip (child_dadosBasicos, child_detalhamento):
                try:
                    atributos[contador].append((nomes,i[0].attributes[arg].value)) #Tenta buscar o atributo na primeira child, se não for encontrado parte para o segundo
                except KeyError:
                    atributos[contador].append((nomes,j[0].attributes[arg].value))
        
        for i in range(len(atributos)):
            dic[atributos_Tag[i]] = atributos[i] #Adiciona para cada chave a tupla contendo todos elementos da sublista em questão
        
        return dic
            
    eventos = extrair_info(filename, 'TRABALHO-EM-EVENTOS', 'DADOS-BASICOS-DO-TRABALHO', 'DETALHAMENTO-DO-TRABALHO', 'TITULO-DO-TRABALHO', 'ANO-DO-TRABALHO', 'TITULO-DOS-ANAIS-OU-PROCEEDINGS', 'DOI')
    artigos = extrair_info(filename,'ARTIGO-PUBLICADO','DADOS-BASICOS-DO-ARTIGO', 'DETALHAMENTO-DO-ARTIGO', 'TITULO-DO-ARTIGO', 'ANO-DO-ARTIGO', 'TITULO-DO-PERIODICO-OU-REVISTA', 'DOI')
    capitulos = extrair_info(filename, 'CAPITULO-DE-LIVRO-PUBLICADO', 'DADOS-BASICOS-DO-CAPITULO', 'DETALHAMENTO-DO-CAPITULO', 'TITULO-DO-CAPITULO-DO-LIVRO', 'ANO', 'TITULO-DO-LIVRO', 'DOI')
    apresentacoes = extrair_info(filename, 'APRESENTACAO-DE-TRABALHO', 'DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO', 'DETALHAMENTO-DA-APRESENTACAO-DE-TRABALHO', 'TITULO', 'ANO', 'NOME-DO-EVENTO', 'CIDADE-DA-APRESENTACAO', 'DOI')
    
    lista = [eventos, artigos, capitulos, apresentacoes]
    
    return lista

def searchWord(model, sentences, porct): # mesma coisa q o searchChar
    Lista = model.split(" ")
    listagrande2 = []
    for i in range(len(sentences)):
        listagrande2.append(sentences[i].split(" "))
    
    contador = 0
    contadorLista = []
    
    for k in range(len(listagrande2)):
        contador = 0
        for i in range(len(Lista)):
            for j in range (len(listagrande2[k])):
                if Lista[i] == listagrande2[k][j]:
                    contador+=1
                if Lista[i].lower() == listagrande2[k][j]:
                    contador+=1
                if Lista[i].upper() == listagrande2[k][j]:
                    contador+=1
                
        contadorLista.append(contador)

    if max(contadorLista) <= ((porct/100)*len(Lista)):
        contadorLista, listagrande2 = None
    return contadorLista, listagrande2



def searchChar(alcance, modelo, sentence, porct): #Alcance é quantas palavras o código vai analisar, modelo é a sentença desejada, sentence é o conjunto
    #de todas sentenças, porct é a porcentagem do quanto as palavras precisam ser próximas
    
    try:
        palavra = searchWord(modelo, sentence, porct)
        
    

        
        copyPalavra = palavra[0][:] #Serve para encontrar o índice das palavras que mais combinam
        copyPalavra.sort()
        copyPalavra.reverse()
        
        
        lista1 = []
        listaPalavras = []
        
        for i in range(alcance):
            lista1.append(palavra[0].index(copyPalavra[i]))
            
        for i in lista1:
            listaPalavras.append(palavra[1][i])
        
            
        modelo2 = list(modelo)
        modelo2.remove(" ")
        contador = 0
        contadorLista = []
            
        for j in range(len(listaPalavras)):
            contador = 0
            for i in range(len(modelo2)):
                for k in range(len(listaPalavras[j])):
                    for l in range(len(listaPalavras[j][k])):
                        if modelo2[i] == listaPalavras[j][k][l]:
                            contador+=1
            contadorLista.append(contador)
        
        provavelStr = contadorLista.index(max(contadorLista))
        teste1 = " ".join(listaPalavras[provavelStr])
        
        maior_indice = palavra[1].index(teste1.split(" "))

        return teste1, maior_indice
    except TypeError:
        return "Não consta"
    
def runAll(dic_geral, filename, nomes_completos): #Só um "procedimento" pra rodar o código

    dic_geral = juntar_professores(filename, nomes_completos)
    lista_an = []
    lista_an2 = []
    
    for i in range(len(dic_geral[0])):
        for j in range(len(dic_geral[3][i]["NOME-DO-EVENTO"])):
            lista_an.append(dic_geral[3][i]["NOME-DO-EVENTO"][j][1])
        lista_an2.append(lista_an)
        lista_an = []

    
    
    df = pd.ExcelFile('../Qualis_Evento.xlsx').parse('Qualis2019') 
    x=[]
    y=[]
    x.append(df['Nome Padrão'])
    y.append(df['Qualis Final'])
    
    
    teste_lista = []
    teste_dic = {}
    lista_extrato = []
    lista_extrato2 = []
    
    for i in range (len(lista_an2)):
        for j in (lista_an2[i]):
            teste1 = searchChar(2,j,x[0],85)
            
            if teste1 == "Não consta":
                lista_extrato.append("Não consta")
            else:
                lista_extrato.append(y[0][teste1[1]])
            
            
            teste_lista.append(teste1[0])
            
        dic_geral[3][i]["EXTRATO"] = lista_extrato
        teste_dic[nomes_completos[i]] = teste_lista
        teste_lista = []
        lista_extrato2.append(lista_extrato)
        lista_extrato = []
    
    return dic_geral

def anexar_qualis_artigos():
    pass

def anexar_qualis_eventos():
    pass

def escrever_csv():
    pass

def menu_principal():
    # descompactar zips
    path = 'D:/Documents/UFPA/Bloco II/Programação I/Tarefa de arquivos/ufpa-lattes-xml/lattes'
    descompactar(path)
    
    # extrair filenames e nomes completos, renomear xmls
    filenames, nomesCompletos = get_filenames_nomesCompletos(path)
    renomearXmls(path, filenames)
    
    # obter o dicionario de professores
    dic_geral = juntar_professores(filenames, nomesCompletos)
    teste = runAll(dic_geral, filenames, nomesCompletos)
    print(teste)

menu_principal()