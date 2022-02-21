import pytorch_lightning as pl
import torch
from transformers import BertModel,get_linear_schedule_with_warmup, AdamW, BertTokenizerFast as BertTokenizer
from torchmetrics.functional import f1, auroc
import mlflow
from pprint import pprint

from intent_recognition.config.core import config 

class ModelModule(pl.LightningModule):
    def __init__(self, step_per_epoch:int=None) -> None:
        super().__init__()
        self.bert = BertModel.from_pretrained(config.model_config.model_config, return_dict=True)
        #BertModel.from_pretrained(, return_dict=True)
        self.cls = torch.nn.Linear(self.bert.config.hidden_size, config.model_config.num_class)
        self.criterion = torch.nn.BCELoss()
        self.step_per_epoch = step_per_epoch
    
    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        outputs = self.cls(outputs.pooler_output)
        outputs = torch.sigmoid(outputs)

        loss=0
        if labels is not None:
            loss = self.criterion(outputs, labels.float())
        
        return loss, outputs
    
    def step_run(self, batch, stage):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['labels']
        loss, outputs = self(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        self.log(f'{stage}_loss', loss, prog_bar=True, logger=True)

        if stage in ['train', 'test']:
            return {'loss': loss, 'predictions': outputs.detach().detach().cpu(), 'labels': labels.detach().detach().cpu()}
        return loss
    
    def training_step(self, batch, batch_ids):
        return self.step_run(batch, 'train')
    
    def validation_step(self, batch, batch_ids):
        return self.step_run(batch, 'val')
    
    def test_step(self, batch, batch_ids):
        return self.step_run(batch, 'test')
    
    def training_epoch_end(self, outputs):
        predictions =[]
        labels = []

        for output in outputs:
            for label in output['labels']:
                labels.append(label)
            
            for pred in output['predictions']:
                predictions.append(pred)
        labels  = torch.stack(labels).int()
        predictions  = torch.stack(predictions)

        for i, name in enumerate(config.model_config.intents):
            au_roc = auroc(predictions[:, i], labels[:, i])
            #print(f'{name}_roc_auc/Trainn: ', au_roc)
            pprint(f'{name}_roc_auc/Trainn: {str(round(float(au_roc), 2))}', indent=4)
    
    def test_epoch_end(self, outputs):
        predictions =[]
        labels = []

        for output in outputs:
            for label in output['labels']:
                labels.append(label)
            
            for pred in output['predictions']:
                predictions.append(pred)
        labels  = torch.stack(labels).int()
        predictions  = torch.stack(predictions)

        f1_score = f1(predictions,  labels, average='weighted',  num_classes=config.model_config.num_class)
        mlflow.log_metric('f1_score', round(float(f1_score), 2))
        self.log('f1_score', round(float(f1_score), 2), on_epoch=True)
    
    def configure_optimizers(self):
        optim = AdamW(self.parameters(), lr=1e-5)
        warmup_step = self.step_per_epoch // 3
        total_steps = self.step_per_epoch  * config.model_config.batch_size - warmup_step
        scheduler = get_linear_schedule_with_warmup(
           optim,
           0,
            total_steps
        )

        return [optim], [scheduler]

