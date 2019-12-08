## def menu_principal  
Deve montar um procedimento para uma CLI (Command Line Interface) para interação com o usuário e juntar os diversos trechos de código.  
O usuário deve ser capaz de escrever o caminho para a pasta ‘lattes’ onde estão localizados os arquivos compactados baixados diretamente do Lattes. Se o caminho não existir, exibir mensagem de erro e pedir novamente o caminho. Caso contrário, deve exibir o nome e quantidade de arquivos e pedir uma confirmação do usuário.  
Em seguida chamar a função def descompactar com o caminho absoluto da pasta como argumento.  
Chame a função def extrair_nomes, também com o caminho absoluto da pasta como argumento, agora com arquivos extraídos. Essa função retorna duas listas que devem ser guardadas nas variáveis NOMES-COMPLETOS e FILENAMES, respectivamente.  
Chame a função def juntar_professores passando as duas variáveis como argumentos. Essa função retorna 4 dicionários que devem ser guardados nas variáveis EVENTOS, ARTIGOS, CAPITULOS E APRESENTACOES, respectivamente.  
Chame a função def anexar_qualis_artigos passando o dicionário ARTIGOS e o caminho para o pdf de qualis. Essa função retorna o mesmo dicionário, só que modificado, então basta sobrescrever a mesma variável.  
Chame a função def anexar_qualis_eventos passando o dicionário EVENTOS e o caminho para o xlsx de qualis. Essa função retorna o mesmo dicionário, só que modificado, então basta sobrescrever a mesma variável.  
Por fim, chame a função def escrever_csv, que irá criar o csv final.  

## def descompactar  
Recebe o caminho da pasta de currículos.  
Extraia cada arquivo curriculo.xml para uma pasta diferente. Por exemplo, o arquivo do Claudomiro está com o nome ‘4742268936279649.zip’, logo o programa deve extrair o conteúdo do zip para a pasta lattes, de forma que: lattes/4742268936279649/curriculo.xml.  
Não retorna nada, é apenas um procedimento.  

## def extrair_nomes  
Recebe o caminho da pasta de currículos.  
Para cada arquivo na pasta de currículos, deve acessar os Dados Gerais do professor, extrair o nome completo do professor, e guardar em uma lista NOMES-COMPLETOS. Isso pode ser feito de forma semelhante à função def extrair_info, só que apenas para os nomes.  
Em seguida deve renomear o arquivo com o nome completo do professor, onde espaços são substituídos por underscores e trocando letras com acentos por suas correspondentes sem acento. Guardar cada nome de arquivo em uma lista FILENAMES. Por exemplo, André Figueira Riker →
Andre_Figueira_Riker.xml.  
Em seguida, mova o arquivo renomeado para um nível acima, retirando da pasta em que ele foi extraído. Por exemplo, o arquivo do Claudomiro localizado em ‘lattes/4742268936279649/curriculo.xml’, deve ficar em ‘lattes/Claudomiro_de Souza_de_Sales_Junior.xml’. Delete as pastas vazias.  
Retorne as listas NOMES-COMPLETOS e FILENAMES.  

## def juntar_professores  
Recebe as lista de NOMES-COMPLETOS E FILENAMES.  
Crie uma lista vazia para cada categoria de publicação, conforme a saída de def extrair_info: TRABALHOS-EM-EVENTOS; ARTIGOS-PUBLICADOS
CAPITULOS-DE-LIVROS-PUBLICADOS; APRESENTACOES-DE-TRABALHOS.  
Cada lista irá posteriormente conter um dicionário com as informações de todos os professores.  
Em seguida, para cada par de elemento das listas, chame a função def extrair_info, passando como argumentos o nome completo e o filename. Isso retorna uma lista com 4 dicionários, contendo as informações de um único professor. Para cada dicionário, insira a lista de uma categoria na lista geral criada anteriormente. Assim, todos os artigos publicados pelo professor X serão inseridos na lista geral de artigos, e assim por diante. Ordene por ordem alfabética dos nomes dos professores.  
Retorne uma lista com os 4 dicionários gerais.  

## def extrair_info  
Recebe duas strings das listas de NOMES-COMPLETOS e FILENAMES (ver def extrair_nomes).  
A função está quase pronta (ver Código Base), mas deve-se otimizar a função para receber apenas as strings acima. Note que nesse momento a função é chamada do lado de fora passando diversas strings pra busca no xml. Essas strings devem ser posicionadas dentro do corpo da função e retornar os valores para cada variável.  
Para cada arquivo, extrair os 4 dicionários de informações: TRABALHOS-EM-EVENTOS; ARTIGOS-PUBLICADOS; CAPITULOS-DE-LIVROS-PUBLICADOS
APRESENTACOES-DE-TRABALHOS.  
Para cada dicionário, adicionar uma coluna com o nome do professor quantas vezes forem necessárias. Por exemplo, se um professor tiver 6 artigos publicados, faça uma lista NOME-COMPLETO contendo os 6 nomes completos repetidos e insira na primeira posição do dicionário de ARTIGOSPUBLICADOS. 
Retorne uma lista com os 4 dicionários para um único professor.  

## def anexar_qualis_artigos  
Recebe o dicionário ARTIGOS-PUBLICADOS (ver def juntar_professores) e o caminho para o arquivo ‘QUALIS_Periodico.pdf’, presente no Sigaa.  
Leia o pdf em Python usando a biblioteca PyPDF2. Obtenha um dicionário cujas chaves serão ISSN, TITULO e EXTRATO.  
Para cada periódico descrito em TITULO-DO-PERIODICO-OU-REVISTA, verifique o extrato correspondente do pdf. Caso não seja encontrado, adicione ‘não consta’ ao extrato.  
Retorne o dicionário ARTIGOS-PUBLICADOS com uma coluna de extratos correspondentes.  
Verifique a quantidade de extratos inexistentes. Caso seja um número elevado, considere fazer os passos opcionais a seguir.  
(Opcional) Implemente um algoritmo de distância de strings na comparação entre o nome do periódico e o pdf, com o intuito de reduzir a quantidade de extratos que não constam por erro de digitação do professor.  
(Opcional) Traduza o nome do periódico de português → inglês ou vice-versa, com o intuito de reduzir a quantidade de extratos que não constam por escolha de um idioma específico. Verifique a biblioteca Googletrans.  

## def anexar_qualis_eventos  
Recebe o dicionário TRABALHOS-EM-EVENTOS (ver def juntar_professores) e o caminho para o arquivo ‘Qualis_Evento.xlsx’, presente no Sigaa.  
Leia o xls em Python usando a biblioteca openpyxl. Obtenha um dicionário cujas chaves serão SIGLA, NOME-PADRÃO e EXTRATO.
Para cada periódico descrito em TITULO-DOS-ANAIS-OU-PROCEEDINGS, verifique o qualis correspondente do xls. Caso não seja encontrado, adicione ‘não consta’ ao extrato.  
Retorne o dicionário TRABALHOS-EM-EVENTOS com uma coluna de extratos correspondentes.  
Verifique a quantidade de extratos inexistentes. Caso seja um número elevado, considere fazer os passos opcionais a seguir.  
(Opcional) Implemente um algoritmo de distância de strings na comparação entre o nome do periódico e o xls, com o intuito de reduzir a quantidade extratos que não constam por erro de digitação do professor.  
(Opcional) Traduza o nome do periódico de português -> inglês ou vice-versa, com o intuito de reduzir a quantidade de extratos que não constam por escolha de um idioma específico. Verifique a biblioteca Googletrans.  

## def escrever_csv  
Recebe os 4 dicionários pós-extrato (TRABALHOS-EM-EVENTOS, ARTIGOS-PUBLICADOS, CAPITULOS-DE-LIVROS-PUBLICADOS e APRESENTACOESDE-TRABALHOS).  
Crie um arquivo csv e escreva cada categoria em uma planilha separada. Verifique se a formatação dos caracteres está correta no arquivo final.  
Printe uma mensagem informando que a extração foi concluída e que o usuário pode verificar a pasta para visualizar o arquivo.
