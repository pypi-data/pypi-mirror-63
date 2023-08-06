# NodLabsNNS pip package

Nod Labs AutoML package for neural architecture search and model training of image classification

## Requirements
* Access to Cloud TPUs ([Official Cloud TPU Tutorial](https://cloud.google.com/tpu/docs/tutorials/mnasnet))
* Tensorflow 1.15
* Python 3.5+

### Specific steps
1. install pip package
```
pip3 install nod-labs-NNS==0.0.1
```
2. Setting up ImageNet dataset

To setup the ImageNet follow the instructions from [here](https://cloud.google.com/tpu/docs/tutorials/amoebanet#full-dataset)

3. Use nodlabsNNS package for neural architecture search and train

create a python file

Search

```
import nns

model = model.nod_detection('tpu','your-tpu-name','your-bucket-name')
model.dataset('imagenet')
model.search_model()
```
Train
```
import nns

model = model.nod_detection('tpu','your-tpu-name','your-bucket-name')
model.dataset('imagenet')
model.train_model()
```
Currently nns only support TPU for searching and training and only support IMAGENET dataset.






