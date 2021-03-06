import os
import torch
import threading
from common.setting import BASE_ROOT, DATA_ROOT

FEW_SHOT_LEARNING_BASE_ROOT = os.path.dirname(os.path.dirname(__file__)) #few_shot_learning
MODEL_ROOT = os.path.join(BASE_ROOT,'model')
LOG_ROOT = os.path.join(BASE_ROOT,'logs')

#uses a class instead of using parser
class arguments(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        '''
        ////////:param resplit: replit the data
        :param sequential: use sequential sampler instead of episodic
        :param trainval: validation set is merged to the trainning set if True

        :param weight_decay_every: num of epoches for every weight decay
        :param patient: num of epoches to wait before validation begin

        '''
        #if use cuda
        self.cuda = torch.cuda.is_available()
        self.cuda_devide = 1
        self.multigpu = False
        self.random_seed = 1234

        #data args
        #self.resplit = False
        self.dataset = 'omniglot'
        self.dataset_dir = os.path.join(DATA_ROOT, self.dataset)
        self.split_dir = os.path.join(self.dataset_dir, 'splits')
        self.split_name = 'vinyals'
        self.train_split_mode = ['train','val']
        self.sequential = False
        self.train_way = 60
        self.train_shot = 5
        self.train_query = 5
        self.test_way = 5
        self.test_shot = self.train_shot
        self.test_query = 15
        self.train_episodes = 100
        self.test_episodes = 100
        self.trainval =False

        #model args
        self.model_name = 'protonet_conv'
        self.input_size = [1,28,28]
        self.hidden_size = 64
        self.output_size = 64


        #train args
        #self.batch_size #in few shot learning, episode is used
        self.train_epoches = 10000
        self.optim_method = 'torch.optim.Adam'
        self.optim_config = { 'lr': 0.001,'weight_decay': 0.0} #other config should be set in main
        self.weight_decay_every = 20
        self.patient = 1000

        #log args
        res_dir = os.path.join(FEW_SHOT_LEARNING_BASE_ROOT, 'results')
        self.models_dir = os.path.join(res_dir,'models')
        self.logs_dir =  os.path.join(res_dir, 'logs')
        self.trace_fields = ['loss','accuracy']
        self.trace_dir = os.path.join(res_dir,'traces')

        self.model_filename = self.model_name + '.pht'
        self.log_filename = 'log.txt'
        self.trace_filename = 'trace.json'
        self.check_dir(res_dir, self.models_dir, self.logs_dir, self.trace_dir)


    # sigleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(arguments, "_instance"):
            with arguments._instance_lock:
                if not hasattr(arguments, "_instance"):
                    arguments._instance = object.__new__(cls)
        return arguments._instance

    def check_dir(self,*dirs):
        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d) 
                print('dir {} is not exist and it is made now'.format(d))

    def to_dict(self):
        return vars(self)
args = arguments()
