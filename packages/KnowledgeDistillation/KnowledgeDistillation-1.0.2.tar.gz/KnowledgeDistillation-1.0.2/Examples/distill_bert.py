"""
This is a simple example to distill a samll bert bu bigger bert

"""
import torch
import logging
import numpy as np
from transformers import BertModel, BertConfig
from torch.utils.data import DataLoader, RandomSampler, TensorDataset

from knowledge_distillation import KnowledgeDistiller, MultiLayerBasedDistillationLoss
from knowledge_distillation import MultiLayerBasedDistillationEvaluator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Some global variables
train_batch_size = 40
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
learning_rate = 1e-5
num_epoch = 10
# Teacher Model
bert_config = BertConfig(num_hidden_layers=12, output_hidden_states=True, output_attentions=True)
teacher_model = BertModel(bert_config)
# Student Model
bert_config = BertConfig(num_hidden_layers=3, output_hidden_states=True, output_attentions=True)
student_model = BertModel(bert_config)

### Train data loader
input_ids = torch.LongTensor(np.random.randint(100, 1000, (100000, 50)))
attention_mask = torch.LongTensor(np.ones((100000, 50)))
token_type_ids = torch.LongTensor(np.zeros((100000, 50)))
train_data = TensorDataset(input_ids, attention_mask, token_type_ids)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=train_batch_size)


### Train data adaptor
### It is a function that turn batch_data (from train_dataloader) to the inputs of teacher_model and student_model
### You can define your own train_data_adaptor. Remember the input must be device and batch_data.
###  The output is either dict or tuple, but must be consistent with you model's input
def train_data_adaptor(device, batch_data):
    batch_data = tuple(t.to(device) for t in batch_data)
    batch_data_dict = {"input_ids": batch_data[0],
                       "attention_mask": batch_data[1],
                       "token_type_ids": batch_data[2], }
    # In this case, the teacher and student use the same input
    return batch_data_dict, batch_data_dict


### The loss model is the key for this generation.
### We have already provided a general loss model for distilling multi bert layer
### In most cases, you can directly use this model.
#### First, we should define a distill_config which indicates how to compute ths loss between teacher and student.
#### distill_config is a list-object, each item indicates how to calculate loss.
#### It also defines which output of which layer to calculate loss.
#### type "ts_distill" means that we compute loss between teacher and student
#### type "hard_distill" means that we compute loss between student output and ground truth

distill_config = [
    {"teacher_layer_name": "embedding_layer", "teacher_layer_output_name": "embedding",
     "student_layer_name": "embedding_layer", "student_layer_output_name": "embedding",
     "loss": {"loss_function": "mse_with_mask", "args": {}}, "weight": 1.0
     },
    {"teacher_layer_name": "bert_layer4", "teacher_layer_output_name": "hidden_states",
     "student_layer_name": "bert_layer1", "student_layer_output_name": "hidden_states",
     "loss": {"loss_function": "mse_with_mask", "args": {}}, "weight": 1.0
     },
    {"teacher_layer_name": "bert_layer8", "teacher_layer_output_name": "hidden_states",
     "student_layer_name": "bert_layer2", "student_layer_output_name": "hidden_states",
     "loss": {"loss_function": "mse_with_mask", "args": {}}, "weight": 1.0
     },
    {"type": "ts_distill",
     "teacher_layer_name": "bert_layer12", "teacher_layer_output_name": "hidden_states",
     "student_layer_name": "bert_layer3", "student_layer_output_name": "hidden_states",
     "loss": {"loss_function": "mse_with_mask", "args": {}}, "weight": 1.0
     },
    {"teacher_layer_name": "bert_layer4", "teacher_layer_output_name": "attention",
     "student_layer_name": "bert_layer1", "student_layer_output_name": "attention",
     "loss": {"loss_function": "attention_mse_with_mask", "args": {}}, "weight": 1.0
     },

    {"teacher_layer_name": "bert_layer8", "teacher_layer_output_name": "attention",
     "student_layer_name": "bert_layer2", "student_layer_output_name": "attention",
     "loss": {"loss_function": "attention_mse_with_mask", "args": {}}, "weight": 1.0
     },
    {"teacher_layer_name": "bert_layer12", "teacher_layer_output_name": "attention",
     "student_layer_name": "bert_layer3", "student_layer_output_name": "attention",
     "loss": {"loss_function": "attention_mse_with_mask", "args": {}}, "weight": 1.0
     },
    {"teacher_layer_name": "pred_layer", "teacher_layer_output_name": "pooler_output",
     "student_layer_name": "pred_layer", "student_layer_output_name": "pooler_output",
     "loss": {"loss_function": "mse", "args": {}}, "weight": 1.0
     },
]


### teacher_output_adaptor and student_output_adaptor
### In most cases, model's output is tuple-object, However, in our package, we need the output is dict-object,
### like: { "layer_name":{"output_name":value} .... }
### Hence, the output adaptor is to turn your model's output to dict-object output
### In my case, teacher and student can use one adaptor
def output_adaptor(model_output):
    last_hidden_state, pooler_output, hidden_states, attentions = model_output
    output = {"embedding_layer": {"embedding": hidden_states[0]}}
    for idx in range(len(attentions)):
        output["bert_layer" + str(idx + 1)] = {"hidden_states": hidden_states[idx + 1],
                                               "attention": attentions[idx]}
    output["pred_layer"] = {"pooler_output": pooler_output}
    return output


# loss_model
loss_model = MultiLayerBasedDistillationLoss(distill_config=distill_config,
                                             teacher_output_adaptor=output_adaptor,
                                             student_output_adaptor=output_adaptor)
# optimizer
param_optimizer = list(student_model.named_parameters())
no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
    {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]
optimizer = torch.optim.Adam(params=optimizer_grouped_parameters, lr=learning_rate)
# evaluator
# this is a basic evalator, it can output loss value and save models
evaluator = MultiLayerBasedDistillationEvaluator(save_dir="save_model", save_step=1000, print_loss_step=20)
# Get a KnowledgeDistiller
distiller = KnowledgeDistiller(teacher_model=teacher_model, student_model=student_model,
                               train_dataloader=train_dataloader, dev_dataloader=None,
                               train_data_adaptor=train_data_adaptor, dev_data_adaptor=None,
                               device=device, loss_model=loss_model, optimizer=optimizer,
                               evaluator=evaluator, num_epoch=num_epoch)
# start distillate
distiller.distillate()
