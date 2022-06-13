from pydoc import cli
from time import sleep
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import json



def copiarFatura(request, codFatura):
    context = {}
    codigoFatura = codFatura
    codigoFatura = str(codigoFatura)
    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
    token = json.loads(tokenMK.content)
    token = token["Token"]

    digitavel = requests.get('https://mksf.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
    digitavel = json.loads(digitavel.content)
    digitavel = digitavel['DadosFatura'][0]
 

    context['digitavel'] = digitavel
    return render(request, 'digitavel.html', context=context)


def buscarCliente(request):
    if request.method == 'POST':
        context = {}
        doc = request.POST.get('doc', '')
        doc = doc.replace('.', '')
        doc = doc.replace('-', '')
        doc = doc.replace('/', '')
        if (len(doc) < 11):
            print('cheguei aqui')
            return render(request, 'error.html')
        else:            
            tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
            token = json.loads(tokenMK.content)
            token = token["Token"]
            cliente = requests.get('https://mksf.infolic.net.br/mk/WSMKConsultaDoc.rule?sys=MK0&token='+token+'&doc='+doc)
            cliente = cliente.json()
            if (len(cliente) == 3):
                tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
                token = json.loads(tokenMK.content)
                token = token["Token"]
                cliente = requests.get('https://mkcampos.infolic.net.br/mk/WSMKConsultaDoc.rule?sys=MK0&token='+token+'&doc='+doc)
                cliente = cliente.json()    
                if (len(cliente) == 3):
                    return render(request, 'error.html')
            
                if (cliente['Outros'] == []):
                    CodigoPessoa = cliente['CodigoPessoa']     
                    CodigoPessoa = str(CodigoPessoa)       
                    tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
                    token = json.loads(tokenMK.content)
                    token = token["Token"]
                    faturas = requests.get('https://mkcampos.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
                    faturas = json.loads(faturas.content)
                    codigos = faturas['FaturasPendentes']
                    context['faturas'] = faturas
                    index = 0
                    
                    for codFatura in codigos:
                        codigoFatura = str(codFatura['codfatura'])
                        tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
                        token = json.loads(tokenMK.content)
                        token = token["Token"]
                        digitavel = requests.get('https://mkcampos.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
                        digitavel = json.loads(digitavel.content)
                        digitavel = digitavel['DadosFatura'][0]
                        digitavel = {'ld':digitavel['ld']}
                        context['faturas']['FaturasPendentes'][index].update(digitavel)
                        index +=1
                        

                    print(context)
                    
                          
                    return render(request, 'listadefaturas.html', context=context)
                else:
                    context['clientes'] = cliente
                    return render(request, 'endereco.html', context=context)
            else:
                if (cliente['Outros'] == []):
                    CodigoPessoa = cliente['CodigoPessoa']     
                    CodigoPessoa = str(CodigoPessoa)       
                    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
                    token = json.loads(tokenMK.content)
                    token = token["Token"]
                    faturas = requests.get('https://mksf.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
                    faturas = json.loads(faturas.content)
                    codigos = faturas['FaturasPendentes']
                    context['faturas'] = faturas
                    index = 0
                    
                    for codFatura in codigos:
                        codigoFatura = str(codFatura['codfatura'])
                        tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
                        token = json.loads(tokenMK.content)
                        token = token["Token"]
                        digitavel = requests.get('https://mksf.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
                        digitavel = json.loads(digitavel.content)
                        digitavel = digitavel['DadosFatura'][0]
                        digitavel = {'ld':digitavel['ld']}
                        context['faturas']['FaturasPendentes'][index].update(digitavel)
                        index +=1
                        
                    context['faturas'] = faturas
                    return render(request, 'listadefaturas.html', context=context)
                else:
                    context['clientes'] = cliente
                    return render(request, 'endereco.html', context=context)

def listarFaturas(request, CodigoPessoa):
    context = {}
    CodigoPessoa = str(CodigoPessoa)
    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
    token = json.loads(tokenMK.content)
    token = token["Token"]
    faturas = requests.get('https://mksf.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
    faturas = json.loads(faturas.content)
    context['faturas'] = faturas
    return render(request, 'listadefaturas.html', context=context)             

def imprimirFatura(request, codFatura):
    context = {}
    codigoFatura = codFatura
    codigoFatura = str(codigoFatura)
    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
    token = json.loads(tokenMK.content)
    token = token["Token"]

    urlFtura = requests.get('https://mksf.infolic.net.br/mk/WSMKSegundaViaCobranca.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
    urlFtura = json.loads(urlFtura.content)
    urlFtura = urlFtura['PathDownload']
    return HttpResponseRedirect(urlFtura)

