from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import json

from pages.models import Solicitacoes



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
            return render(request, 'error.html')
        else:            
            tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
            token = json.loads(tokenMK.content)
            token = token["Token"]
            clienteSf = requests.get('https://mksf.infolic.net.br/mk/WSMKConsultaDoc.rule?sys=MK0&token='+token+'&doc='+doc)
            clienteSf = clienteSf.json()
            
            tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
            token = json.loads(tokenMK.content)
            token = token["Token"]
            clienteRegional = requests.get('https://mkcampos.infolic.net.br/mk/WSMKConsultaDoc.rule?sys=MK0&token='+token+'&doc='+doc)
            clienteRegional = clienteRegional.json()    
            
            if (len(clienteSf) == 3 and len(clienteRegional) == 3):
                return render(request, 'error.html')
            
            elif(len(clienteSf) > 3 and len(clienteRegional) > 3):
                context['clienteSf'] = clienteSf
                context['clienteRegional'] = clienteRegional
                return render(request, 'endereco.html', context=context)
            
            if (len(clienteSf) == 3):                            
                if (clienteRegional['Outros'] == []):
                    CodigoPessoa = clienteRegional['CodigoPessoa']     
                    CodigoPessoa = str(CodigoPessoa)       
                    tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
                    token = json.loads(tokenMK.content)
                    token = token["Token"]
                    faturasRegional = requests.get('https://mkcampos.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
                    faturasRegional = json.loads(faturasRegional.content)
                    codigos = faturasRegional['FaturasPendentes']
                    context['faturasRegional'] = faturasRegional
                    index = 0
                    for codFatura in codigos:
                        if (codFatura['contratos'] != None):
                            codigoFatura = str(codFatura['codfatura'])
                            tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
                            token = json.loads(tokenMK.content)
                            token = token["Token"]
                            digitavelRegional = requests.get('https://mkcampos.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
                            digitavelRegional = json.loads(digitavelRegional.content)
                        
                            if (len(digitavelRegional)!= 3):
                                digitavelRegional = digitavelRegional['DadosFatura'][0]
                                digitavelRegional = {'ld':digitavelRegional['ld']}
                                context['faturasRegional']['FaturasPendentes'][index].update(digitavelRegional)
                                index +=1
                            else:
                                digitavelRegional = {'ld':'None'}
                                context['faturasRegional']['FaturasPendentes'][index].update(digitavelRegional)
                                index +=1
                    
                    context['clienteRegional'] = clienteRegional
                    
                    return render(request, 'listadefaturas.html', context=context)
                else:
                    context['clienteRegional'] = clienteRegional
                    return render(request, 'endereco.html', context=context)
            else:
                if (clienteSf['Outros'] == []):
                    CodigoPessoa = clienteSf['CodigoPessoa']     
                    CodigoPessoa = str(CodigoPessoa)       
                    
                    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
                    token = json.loads(tokenMK.content)
                    token = token["Token"]
                    faturasSf = requests.get('https://mksf.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
                    faturasSf = json.loads(faturasSf.content)
                    codigos = faturasSf['FaturasPendentes']
                    context['faturasSf'] = faturasSf
                    index = 0
                    for codFatura in codigos:
                        if (codFatura['contratos'] != None):
                            codigoFatura = str(codFatura['codfatura'])
                            tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
                            token = json.loads(tokenMK.content)
                            token = token["Token"]
                            digitavelSf = requests.get('https://mksf.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
                            digitavelSf = json.loads(digitavelSf.content)                            
                            if (len(digitavelSf)!= 3):
                                digitavelSf = digitavelSf['DadosFatura'][0]
                                digitavelSf = {'ld':digitavelSf['ld']}
                                context['faturasSf']['FaturasPendentes'][index].update(digitavelSf)
                                index +=1
                            else:
                                digitavelSf = {'ld':'None'}
                                context['faturasSf']['FaturasPendentes'][index].update(digitavelSf)
                                index +=1
                    context['faturasSf'] = faturasSf
                    
                    return render(request, 'listadefaturas.html', context=context)
                else:
                    context['clienteSf'] = clienteSf
                    return render(request, 'endereco.html', context=context)



def listarFaturasSF(request, CodigoPessoa): 
    context = {}
    CodigoPessoa = str(CodigoPessoa)
    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
    token = json.loads(tokenMK.content)
    token = token["Token"]
    faturasSf = requests.get('https://mksf.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
    faturasSf = json.loads(faturasSf.content)
    codigos = faturasSf['FaturasPendentes']
    context['faturasSf'] = faturasSf
    index = 0
    for codFatura in codigos:
        if (codFatura['contratos'] != None):
            codigoFatura = str(codFatura['codfatura'])
            tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
            token = json.loads(tokenMK.content)
            token = token["Token"]
            digitavelSf = requests.get('https://mksf.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
            digitavelSf = json.loads(digitavelSf.content)                            
            if (len(digitavelSf)!= 3):
                digitavelSf = digitavelSf['DadosFatura'][0]
                digitavelSf = {'ld':digitavelSf['ld']}
                context['faturasSf']['FaturasPendentes'][index].update(digitavelSf)
                index +=1
            else:
                digitavelSf = {'ld':'None'}
                context['faturasSf']['FaturasPendentes'][index].update(digitavelSf)
                index +=1
    context['faturasSf'] = faturasSf
    
    return render(request, 'listadefaturas.html', context=context)             

def listarFaturasCPS(request, CodigoPessoa): 
    context = {}
    CodigoPessoa = str(CodigoPessoa)
    tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
    token = json.loads(tokenMK.content)
    token = token["Token"]
    faturasRegional = requests.get('https://mkcampos.infolic.net.br/mk/WSMKFaturasPendentes.rule?sys=MK0&token='+token+'&cd_cliente='+CodigoPessoa)
    faturasRegional = json.loads(faturasRegional.content)
    codigos = faturasRegional['FaturasPendentes']
    context['faturasRegional'] = faturasRegional
    index = 0
    for codFatura in codigos:
        if (codFatura['contratos'] != None):
            codigoFatura = str(codFatura['codfatura'])
            tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
            token = json.loads(tokenMK.content)
            token = token["Token"]
            digitavelRegional = requests.get('https://mkcampos.infolic.net.br//mk/WSMKLDViaSMS.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
            digitavelRegional = json.loads(digitavelRegional.content)
        
            if (len(digitavelRegional)!= 3):
                digitavelRegional = digitavelRegional['DadosFatura'][0]
                digitavelRegional = {'ld':digitavelRegional['ld']}
                context['faturasRegional']['FaturasPendentes'][index].update(digitavelRegional)
                index +=1
            else:
                digitavelRegional = {'ld':'None'}
                context['faturasRegional']['FaturasPendentes'][index].update(digitavelRegional)
                index +=1
    
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
    cod_pessoa = urlFtura['CodigoPessoa']
    vcto = urlFtura['Vcto']

    if (len(urlFtura) == 3):
        tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
        token = json.loads(tokenMK.content)
        token = token["Token"]
        urlFtura = requests.get('https://mkcampos.infolic.net.br/mk/WSMKSegundaViaCobranca.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)     
        urlFtura = json.loads(urlFtura.content)
        cod_pessoa = urlFtura['CodigoPessoa']
        vcto = urlFtura['Vcto']
        urlFtura = urlFtura['PathDownload']
        objeto = Solicitacoes(cod_cliente=cod_pessoa, venc_Fatura=vcto, imprimiu=True, copiou=False)
        objeto.save()
        return HttpResponseRedirect(urlFtura)
    else:
        urlFtura = urlFtura['PathDownload']
        objeto = Solicitacoes(cod_cliente=cod_pessoa, venc_Fatura=vcto, imprimiu=True, copiou=False)
        objeto.save()
        return HttpResponseRedirect(urlFtura)

def salvarFatura(request, codFatura):
    context = {}
    codigoFatura = codFatura
    codigoFatura = str(codigoFatura)
    tokenMK = requests.get('https://mksf.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=081da7f6f0f9996b3fa88780e4380d3b&password=3109188ce623658&cd_servico=9999')
    token = json.loads(tokenMK.content)
    token = token["Token"]
    urlFtura = requests.get('https://mksf.infolic.net.br/mk/WSMKSegundaViaCobranca.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)
    urlFtura = json.loads(urlFtura.content)
    cod_pessoa = urlFtura['CodigoPessoa']
    vcto = urlFtura['Vcto']

    if (len(urlFtura) == 3):
        tokenMK = requests.get('https://mkcampos.infolic.net.br/mk/WSAutenticacao.rule?sys=MK0&token=641c07fb39ec86c547422769845608c8&password=3514b1c0d243236&cd_servico=9999')
        token = json.loads(tokenMK.content)
        token = token["Token"]
        urlFtura = requests.get('https://mkcampos.infolic.net.br/mk/WSMKSegundaViaCobranca.rule?sys=MK0&token='+token+'&cd_fatura='+codigoFatura)     
        urlFtura = json.loads(urlFtura.content)
        cod_pessoa = urlFtura['CodigoPessoa']
        vcto = urlFtura['Vcto']
        objeto = Solicitacoes(cod_cliente=cod_pessoa, venc_Fatura=vcto, imprimiu=False, copiou=True)
        objeto.save()
        return render(request, 'sucesso.html')  
    else:
        objeto = Solicitacoes(cod_cliente=cod_pessoa, venc_Fatura=vcto, imprimiu=False, copiou=True)
        objeto.save()
        return render(request, 'sucesso.html')  