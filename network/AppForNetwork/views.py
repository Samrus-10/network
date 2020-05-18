from django.shortcuts import render
from django.http import  HttpResponse as Response
from .models import Users , NETWORKS , PARAMS , DESCRIPTIONS , COMMENTS , DATASET , RESULT_TEACHING , FILE_EXEL
import json
import os
#подключение нейронки
from src.src import PipelineBuilder
 
# Create your views here.

def index (request):
    return Response("<h1 align = 'center'>All works</h1>")

# def main(request):
#     return render(request , 'AppForNetwork/main.html')

def enter(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        try:
            enter = Users.objects.get(login = login , password = password)
        except : 
            return Response("Not Exist")

    return Response("{0}:{1}".format(enter.admin , enter.id))


def registration(request):
    
    if request.method == 'POST':
        person = Users()
        person.login = request.POST.get('login')
        person.password = request.POST.get('password')
        person.admin = request.POST.get('admin')
        person.save()

    return Response("sucess")


def NetworkParams(request):
    
    if request.method == 'POST':
        
        id_admin = request.POST.get('id_admin')

        
        network = NETWORKS()
        network.id_admin = Users.objects.get(id = id_admin)
        network.save()

        params = PARAMS()
        params.id_network = network
        params.name = request.POST.get('name')
        params.amount_params = request.POST.get('amount_params')
        params.amount_network = request.POST.get('amount_network')
        params.amount_layers = request.POST.get('amount_layers')
        params.name_function = request.POST.get('name_function')
        params.accuracy = request.POST.get('accuracy')
        params.max_time = request.POST.get('max_time')
        params.classs = request.POST.get('classs')
        params.save()

    return Response('{0}'.format(network.id))


def Text(request):
    
    if request.method == 'POST':
        
        id_network = request.POST.get('id_network')
        network = NETWORKS.objects.get(id = id_network)

        descriptions = DESCRIPTIONS()
        descriptions.id_network = network
        descriptions.short_text = request.POST.get('short_text')
        descriptions.long_text = request.POST.get('long_text')
        descriptions.save()

    return Response('success')


def Comment(request):
    
    if request.method == 'POST':

        id_network = request.POST.get('id_network')
        network = NETWORKS.objects.get(id = id_network)

        lengnth = request.POST.get('length')

        for i in range(int(lengnth)):
            comments = COMMENTS()
            comments.id_network = network
            comments.number_param = i
            comments.comment = request.POST.get('comment_{0}'.format(i))
            comments.save()

    return Response('success')

        
def File_exel(request):
    if request.method == 'POST':

        id_network = request.POST.get('id_network')
        network = NETWORKS.objects.get(id = id_network)

        files = FILE_EXEL()
        files.id_network = network
        files.file = request.FILES['sender_file_exel']
        files.save()

    return Response('success')

def AllNetwork(request):
    networks = NETWORKS.objects.all()
    listNetwork = []
    for net in networks:
        
        name = PARAMS.objects.get(id_network = net.id).name
        short = DESCRIPTIONS.objects.get(id_network = net.id).short_text
        longs = DESCRIPTIONS.objects.get(id_network = net.id).long_text
        comment = COMMENTS.objects.filter(id_network = net.id)
        listComment = []
        for com in comment:
            listComment.append(com.comment)

        dictin = {\
           'id' : net.id , 'name' : name ,'created' : net.id_admin.login ,\
           'short_text':short, 'long_text':longs, 'comments':listComment}
        listNetwork.append(dictin)
    return Response(json.dumps(listNetwork))

#функция обучения нейроной сети 
def NetworkTeaching(request):
    
    if request.method == 'POST':
        id_networks = request.POST.get('id_network')
        network = NETWORKS.objects.get(id = id_networks)
        file = FILE_EXEL.objects.get(id_network = id_networks)
        params = PARAMS.objects.get(id_network = id_networks)
        user = network.id_admin

        n_hiddens = params.amount_params
        n_layers = params.amount_layers
        f_activation = params.name_function
        data_path = os.path.join ( os.path.dirname ( os.path.dirname ( os.path.abspath(__file__)) ) , "{0}".format(file.file) )
        #target_column = params.amount_params
        max_seconds = params.max_time
        min_loss = params.accuracy
        task_type = params.classs
        phase = 'train'
        # seed = ''
        # verbose = ''

        builder = PipelineBuilder()

        # Train
        builder.set_model(n_hiddens, n_layers, f_activation, task_type)
        builder.set_dataset(data_path )#, args.target_column)

        #weights_filename = 'username' + 'netname and idUser' + '.pth' #TODO
        weights_filename = '{0}{1}{2}.pth'.format(user.login , params.name , user.id )
        #logs_filename = 'username' + 'netname' + '.csv' #TODO
        logs_filename = '{0}{1}{2}.csv'.format(user.login , params.name , user.id )
        builder.set_filenames (weights_filename , logs_filename)

        builder.build()

        if args.phase == 'train':
            builder.train(max_seconds , min_loss )
        elif args.phase == 'test':
            builder.test()
        else:
            print('Unknown phase!')

        return Response('{0}'.format(data_path)) 
    

#функция для получение результата от нейроной сети 
def NetworkGivenResult(request):
    #все что ниже это заглушки 
    if request.method == 'POST':
        length = request.POST.get('length')
        array_value_param = []

        for i in range(int(length)):
            array_value_param.append(request.POST.get('param_{0}'.format(i)))

        return Response('{0}'.format(array_value_param))

        