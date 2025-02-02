def initialize_weights(net_l, scale=1):
    if not isinstance(net_l, list):
        net_l = [net_l]
    for net in net_l:
        for m in net.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, a=0, mode='fan_in')
                m.weight.data *= scale  # for residual block
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                init.kaiming_normal_(m.weight, a=0, mode='fan_in')
                m.weight.data *= scale
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias.data, 0.0)


def make_layer(block, n_layers):
    layers = []
    for _ in range(n_layers):
        layers.append(block())
    return nn.Sequential(*layers)


class ResidualBlock_noBN(nn.Module):
    '''Residual block w/o BN
    ---Conv-ReLU-Conv-+-
     |________________|
    '''

    def __init__(self, nf=64):
        super(ResidualBlock_noBN, self).__init__()
        self.conv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)

        # initialization
        initialize_weights([self.conv1, self.conv2], 0.1)

    def forward(self, x):
        identity = x
        out = F.relu(self.conv1(x), inplace=True)
        out = self.conv2(out)
        return identity + out



def calculate_mean_std():

    class MyDataset(Dataset):
        def __init__(self,img_list):
            self.data =img_list

        def __getitem__(self, index):
            #x = self.data[index]
            img=self.data[index]


            return ToTensor()(Image.open(img))

        def __len__(self):
            return len(self.data)


    dataset = MyDataset(img_list)
    loader = DataLoader(
        dataset,
        batch_size=1,
        num_workers=1,
        shuffle=False
    )

    mean = 0.
    std = 0.
    nb_samples = 0.
    i=0
    for data in tqdm(loader):
        #print(type(data))
        batch_samples = data.size(0)
        data = data.view(batch_samples, data.size(1), -1)
        mean += data.mean(2).sum(0)
        std += data.std(2).sum(0)
        nb_samples += batch_samples
        i=i+1
    mean /= nb_samples
    std /= nb_samples

    print(i,mean,std)
    
    
from PIL import Image 
 import numpy as np 
 import os 
 path='/Users/wangzhilin/Downloads/data/RESIDE/ITS/hazy' 
 from torchvision.transforms import transforms as tfs 
 # print(imgs) 
 #cal image mean and stddev 
 def cal_mean_stddev(path,format): 
 width=460 
 height=460 
 files=os.listdir(path) 
 imgs=[] 
 for file in files : 
 if file.find(format)!=-1: 
 img=tfs.Resize((height,width))(Image.open(os.path.join(path,file))) 
 # img.show( 
 # import time 
 # time.sleep(100) 
 img=np.array(img) 
 imgs.append(img) 
 print('total images :%d'%len(imgs)) 
 imgs=np.array(imgs)/255.0 
 print('batch,width,height,channels(RGB)',imgs.shape) 
 m=np.mean(imgs,axis=(0,1,2)) 
 print('mean :R G B',m) 
 # for std : std=std/len(imgs)  
 std=np.zeros(3) 
 for i in range(len(imgs)): 
 std+=np.std(imgs[i],axis=(0,1)) 
 stddev=std/len(imgs) 
 print('stddev:R G B',stddev) 
   if __name__ =='__main__': 
 print(path) 
 cal_mean_stddev(path,'png')
