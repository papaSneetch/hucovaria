from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
import os
from .models import *
import pandas as pd
import mimetypes

def home(request):
	context = {
		'title': 'Home',
		'virusProteins': ['S', 'E', 'M', 'N', 'nsp1', 'nsp2', 'nsp3', 'nsp4', 'nsp5',
						'nsp6', 'nsp7', 'nsp8', 'nsp9', 'nsp10', 'nsp11', 'nsp12', 'nsp13',
						'nsp14', 'nsp15', 'nsp16', 'ORF3a', 'ORF3d', 'ORF6', 'ORF7a',
						'ORF7b', 'ORF8', 'ORF9b', 'ORF9c', 'ORF10'],
		'strains': [
					{'name': 'B.1.1.7', 'label': 'Alpha'},
					{'name': 'B.1.351', 'label': 'Beta'},
					{'name': 'B.1.427', 'label': 'Epsilon'},
					{'name': 'B.1.525', 'label': 'Eta'},
					{'name': 'B.1.526', 'label': 'Iota'},
					{'name': 'B.1.617', 'label': 'Kappa'},
					{'name': 'B.1.617.2', 'label': 'Delta'},
					{'name': 'B.1.617.3', 'label': 'N/A'},
					{'name': 'B.1.621', 'label': 'Mu'},
					{'name': 'P.1', 'label': 'Gamma'},
					{'name': 'P.2', 'label': 'Zeta'},
					{'name': 'Reference', 'label': 'N/A'},
					],
		'annotations': [{'name': 'tissue_expression', 'pprint': 'Tissue Expression'}, {'name': 'localization', 'pprint': 'Localization'}, {'name': 'KEGG', 'pprint': 'KEGG'}],
		'ontologies': ['MF', 'BP', 'CC'],
	}
	return render(request, 'home.html', context)

def about(request):
	context = {
		'title': 'About',
	}
	return render(request, 'about.html', context)

def datasets(request):
	context = {
		'title': 'Datasets',
	}
	return render(request, 'datasets.html', context)

def getInteractionQuerySet(result_id):
	result = Result.objects.get(pk=result_id)
	virus_l = [v.content for v in result.virusresult_set.all()]
	host_l = [h.content for h in result.hostresult_set.all()]
	strains = [s.content for s in result.strainresult_set.all()]
	interactionType = result.interactionresult_set.first()

	qs = Interaction.objects.filter(virus__in=virus_l).filter(host__in=host_l).filter(strain__in=strains)

	return qs

def makeQuery(request):
    strains = ['B.1.1.7',
	    'B.1.351',
	    'B.1.427',
	    'B.1.525',
	    'B.1.526',
	    'B.1.617',
		'B.1.617.2',
		'B.1.617.3',
		'B.1.621',
		'P.1',
		'P.2',
		'Reference']

	#add to Result
    newID = timezone.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

    filename=f'media/{newID}.csv'
    file = f'{newID}.csv'
    annotation = request.POST.get('Annotation')
    if request.POST.get('result_name') == '':
        name = timezone.now()
    else:
        name = request.POST.get('result_name')
    newResult = Result(id=newID, time=timezone.now(), annotation=annotation, name=name)
    newResult.save()

	#add StrainResults
    strains_to_filter = []
    for strain in strains:
        if request.POST.get(strain):
            newStrainResult = StrainResult(result=newResult, content=strain)
            newStrainResult.save()

	#add AnnotationResults
    if annotation == 'KEGG':
        pass
    elif annotation == 'Gene_Ontology':
        pass

	#add HostResults
    for h in request.POST.get('human_prots_text').split(','):
        newHostResult = HostResult(result=newResult, content=h)
        newHostResult.save()


	#add VirusResults
    for v in request.POST.get('hidden_sars_prots').split(','):
        newVirusResult = VirusResult(result=newResult, content=v)
        newVirusResult.save()

	#add InteractionResults
    interactionType = request.POST.get('interaction')
    if interactionType == 'Interolog':
        newInteractionResult = InteractionResult(result=newResult, content=interactionType)
        newInteractionResult.save()
    elif interactionType == 'Domain':
        newInteractionResult = InteractionResult(result=newResult, content=interactionType)
        newInteractionResult.save()

    Interaction_qs = getInteractionQuerySet(newResult.id)
    df = pd.DataFrame(Interaction_qs.values())
    df.to_csv(filename, index=None)
    newResult.file = file
    newResult.save()

    return HttpResponseRedirect(reverse('main:home'))

class ResultsView(generic.ListView):
	template_name = 'results.html'
	context_object_name = 'results'

	for result in Result.objects.all():
		diff = timezone.now() - result.time
		if diff.days > 7:
			os.remove('.' + result.file.url)
			result.delete()


	def get_queryset(self):
		return Result.objects.all().reverse()


class TableView(generic.ListView):
	template_name = 'table.html'
	context_object_name = 'query'
	paginate_by = 100

	def get_queryset(self):
		result_id = self.request.META['PATH_INFO'].split('/')[3]
		annotation = Result.objects.get(pk=result_id).annotation
		qs = getInteractionQuerySet(result_id)
		qs_l = qs.values()
		new = []
		if annotation == 'Gene_Ontology':
			for row in qs_l:
				go = GO.objects.filter(gene=row['host'])
				if len(go) != 0:
					for g in go:
						newrow = row.copy()
						newrow['GO'] = g.name
						newrow['GO_Description'] = g.description
						newrow['GO_Type'] = g.type
						new.append(newrow)
				else:
					newrow = row.copy()
					new.append(newrow)
			return new
		elif annotation == 'KEGG':
			for row in qs_l:
				kegg = KEGG.objects.filter(gene=row['host'])
				if len(kegg) != 0:
					for k in kegg:
						newrow = row.copy()
						newrow['KEGG'] = k.name
						newrow['KEGG_Description'] = k.description
						new.append(newrow)
				else:
					newrow = row.copy()
					new.append(newrow)
			return new

		return qs_l

	def get_context_data(self, **kwargs):
		result_id = self.request.META['PATH_INFO'].split('/')[3]
		context = super().get_context_data(**kwargs)
		annotation = Result.objects.get(pk=result_id).annotation
		context['annotation'] = annotation
		context['title'] = f'Table View - {Result.objects.get(pk=result_id).name}'
		context['subtitle'] = Result.objects.get(pk=result_id).id
		context['result_id'] = result_id
		context['file'] = Result.objects.get(pk=result_id).file
		return context

def network(request, result_id):
	context = {}

	df = pd.read_csv(f'media/{result_id}.csv')
	cols = ['id', 'color']
	virus = df[['virus']].drop_duplicates()
	virus['color'] = ['red' for x in range(len(virus))]
	host = df[['host']].drop_duplicates()
	host['color'] = ['blue' for x in range(len(host))]
	virus.columns=cols
	host.columns=cols
	nodes = pd.concat([virus, host])

	strain_color = {
		'B.1.1.7': '#FF33EE',
		'B.1.351': '#A033FF',
		'B.1.427': '#33C2FF',
		'B.1.525': '#33FFA7',
		'B.1.526': '#33FF41',
		'B.1.617': '#FFF933',
		'B.1.617.2': '#FFA933',
		'B.1.617.3': '#FF7833',
		'B.1.621': '#000000',
		'P.1': '#806C23',
		'P.2': '#A30D5C',
		'Reference': '#0D85A3'
	}
	strain_colors = []

	for k,v in strain_color.items():
		strain_colors.append({'name': k, 'color': v})

	interactions = []
	for index,row in df.iterrows():
		virus = row['virus']
		host = row['host']
		interactions.append({'id': virus + "_" + host + "_" + strain_color[row['strain']], 'source': virus, 'target': host, 'color': strain_color[row['strain']], 'strain': row['strain']})

	context['strain_colors'] = strain_colors
	context['nodes'] = nodes.to_dict('records')
	context['interactions'] = interactions
	context['title'] = f'Network View - {Result.objects.get(pk=result_id).name}'
	context['subtitle'] = Result.objects.get(pk=result_id).id

	return render(request, 'network.html', context)

def downloadFile(request, result_id):
	context = {}
	file = Result.objects.get(pk=result_id).file
	return render(request, file.url, context)
