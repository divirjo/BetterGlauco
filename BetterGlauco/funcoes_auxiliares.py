from decimal import Decimal

class Funcoes_auxiliares():
    '''
    Classe de funções auxiliares, não possui um objeto a ser construído, em razão disso não há o parâmetro self nas declarações dos métodos.
    '''
    
    
    def converte_numero_str(numero_str):
        '''
        Converte uma string em número, substituindo a vírgula dos decimais por ponto.
        
        return 
            float ou integer se for número. Se não for, retorna 0
        '''
        
        if not isinstance(numero_str, str):
            return 0
        
        numero_str = numero_str.strip()
               
        
        if ',' in numero_str:
            numero_str = numero_str.replace('.','').replace(',','.')
        
        try:
            return int(numero_str)
        except:
            pass
        
        try:
            return Decimal(numero_str)
        except:
            return 0
        

    def get_perfil_ativo(request, **kwargs):
        '''
        Obtém o ID do Perfil da conta ativo no módulo investimento
        
        returns: 
            integer com o ID do Perfil ou 0
        '''
        if request.GET.get('perfil'):
            id_perfil = Funcoes_auxiliares.converte_numero_str(request.GET.get('perfil')) 
        elif 'id_perfil_selecionado' in request.session:
            id_perfil = request.session['id_perfil_selecionado']
        else:
            id_perfil = 0
        
        request.session['id_perfil_selecionado'] = id_perfil
        return id_perfil