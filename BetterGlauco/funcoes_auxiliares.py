class Funcoes_auxiliares():
    '''
    Classe de funções auxiliares, não possui um objeto a ser construido, em razão disso não há o parâmetro self nas declarações dos métodos.
    '''
    
    
    def converte_numero_str(numero_str):
        '''
        Converte uma string em número, substituindo a vícula dos decimais por ponto.
        
        return float ou integer se for número. Se não for, retorna 0
        '''
        
        numero_str = numero_str.strip()
               
        if ',' in numero_str:
            numero_str = numero_str.replace('.','').replace(',','.')
        
        try:
            return int(numero_str)
        except:
            pass
        
        try:
            return float(numero_str)
        except:
            return 0
        