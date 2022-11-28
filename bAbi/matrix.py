import torch
import torch.nn.functional as F 

print(torch.cuda.device_count())

keep_running1 = torch.randn(10000, 10000).to('cuda')
while (True):
    keep_running1 = torch.mm(keep_running1, keep_running1, out=None)
    keep_running1 = F.normalize(keep_running1, dim=-1, p=2)