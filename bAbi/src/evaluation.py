import csv
import torch
import torch.nn.functional as F 
from utils import results_headers

def evaluate(ds, run_model, encode_batch, decode_batch, results_fn="results.tsv"):
    # adapted from https://huggingface.co/docs/transformers/model_doc/t5#training

    tsv_file = open(results_fn, 'w+', encoding='utf8', newline='')
    tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
    tsv_writer.writerow(results_headers)

    # keep_running1 = torch.randn(10000, 10000).to('cuda')

    for i, (batch_x, batch_y, batch_metadata) in enumerate(ds.batch(batch_size=32)):
        if (i % 10) == 0: print(i)

        # keep_running1 = torch.mm(keep_running1, keep_running1, out=None)
        # keep_running1 = F.normalize(keep_running1, dim=-1, p=2)

        inputs = encode_batch(batch_x)
        outputs = run_model(inputs)
        answers = decode_batch(outputs)

        for (p, h), e, m, a in zip(batch_x, batch_y, batch_metadata, answers):
            tsv_writer.writerow([p, h, e, *m, a, int(a in e)])
        